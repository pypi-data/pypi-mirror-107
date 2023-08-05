/*
Python bindings for libelas, by Andreas Geiger.

The bindings have been written in May 2021 by Pier Angelo Vendrame.

libelas is free software; you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation; either version 3 of the License, or any later version.

libelas is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
libelas; if not, write to the Free Software Foundation, Inc., 51 Franklin
Street, Fifth Floor, Boston, MA 02110-1301, USA
 */

#include "elas.h"

#include <Python.h>
#include <structmember.h>

#include <numpy/arrayobject.h>
#include <numpy/ndarraytypes.h>

namespace {
struct ElasObject {
	PyObject_HEAD
	Elas::parameters params;
	/* We don't need to store an Elas object, as it only stores
	parameters, of which we already keep a copy, because we cannot
	access them, as they are private. */
};

PyObject *Elas_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
	ElasObject *self = reinterpret_cast<ElasObject *>(type->tp_alloc(type, 0));
	if (self) {
		self->params = Elas::parameters();
	}
	return reinterpret_cast<PyObject *>(self);
}

int Elas_init(ElasObject *self, PyObject *args, PyObject *kwds)
{
	static const char *kwlist[] = {
		"disp_min",
		"disp_max",
		"support_threshold",
		"support_texture",
		"candidate_stepsize",
		"incon_window_size",
		"incon_threshold",
		"incon_min_support",
		"add_corners",
		"grid_size",
		"beta",
		"gamma",
		"sigma",
		"sradius",
		"match_texture",
		"lr_threshold",
		"speckle_sim_threshold",
		"speckle_size",
		"ipol_gap_width",
		"filter_median",
		"filter_adaptive_mean",
		"postprocess_only_left",
		"subsampling",
		nullptr
	};

	int add_corners = self->params.add_corners;
	int filter_median = self->params.filter_median;
	int filter_adaptive_mean = self->params.filter_adaptive_mean;
	int postprocess_only_left = self->params.postprocess_only_left;
	int subsampling = self->params.subsampling;

	if (!PyArg_ParseTupleAndKeywords(args, kwds,
			"|iifiiiiipiffffiifiipppp", const_cast<char **>(kwlist),
			&self->params.disp_min,
			&self->params.disp_max,
			&self->params.support_threshold,
			&self->params.support_texture,
			&self->params.candidate_stepsize,
			&self->params.incon_window_size,
			&self->params.incon_threshold,
			&self->params.incon_min_support,
			&add_corners,
			&self->params.grid_size,
			&self->params.beta,
			&self->params.gamma,
			&self->params.sigma,
			&self->params.sradius,
			&self->params.match_texture,
			&self->params.lr_threshold,
			&self->params.speckle_sim_threshold,
			&self->params.speckle_size,
			&self->params.ipol_gap_width,
			&filter_median,
			&filter_adaptive_mean,
			&postprocess_only_left,
			&subsampling)) {
		return -1;
	}

	self->params.add_corners = add_corners ? 1 : 0;
	self->params.filter_median = filter_median ? 1 : 0;
	self->params.filter_adaptive_mean = filter_adaptive_mean ? 1 : 0;
	self->params.postprocess_only_left = postprocess_only_left ? 1 : 0;
	self->params.subsampling = subsampling ? 1 : 0;

	return 0;
}

/**
 * A helper to automatically release buffers and decrease reference counts
 * when needed.
 */
struct ProcessHelper {
	Py_buffer input1;
	Py_buffer input2;
	PyArrayObject *disparity1 = nullptr;
	PyArrayObject *disparity2 = nullptr;
	Elas elas;
	ElasObject *self;

	ProcessHelper(ElasObject *self) : elas(self->params), self(self)
	{
		memset(&input1, 0, sizeof(input1));
		memset(&input2, 0, sizeof(input2));
	}

	~ProcessHelper()
	{
		PyBuffer_Release(&input1);
		PyBuffer_Release(&input2);

		if (disparity1) {
			Py_DECREF(disparity1);
			disparity1 = nullptr;
		}
		if (disparity2) {
			Py_DECREF(disparity2);
			disparity2 = nullptr;
		}
	}

	PyObject *process(PyObject *args)
	{
		if (!PyArg_ParseTuple(args, "y*y*", &input1, &input2)) {
			return nullptr;
		}

		const int buf_flags = PyBUF_FORMAT | PyBUF_STRIDES | PyBUF_C_CONTIGUOUS;
		if (PyObject_GetBuffer(input1.obj, &input1, buf_flags)
				|| PyObject_GetBuffer(input2.obj, &input2, buf_flags)
				|| !check_buffers()) {
			return nullptr;
		}
		if (!make_output()) {
			return nullptr;
		}

		PyObject *ret = PyTuple_New(2);
		if (!ret) {
			return nullptr;
		}

		const uint8_t *in1 = reinterpret_cast<const uint8_t *>(input1.buf);
		const uint8_t *in2 = reinterpret_cast<const uint8_t *>(input2.buf);
		float *disp1 = reinterpret_cast<float *>(PyArray_DATA(disparity1));
		float *disp2 = reinterpret_cast<float *>(PyArray_DATA(disparity2));
		int32_t dims[] = {
			static_cast<int32_t>(input1.shape[1]),
			static_cast<int32_t>(input1.shape[0]),
			static_cast<int32_t>(input1.strides[0])};
		elas.process(in1, in2, disp1, disp2, dims);

		if (PyTuple_SetItem(ret, 0, reinterpret_cast<PyObject *>(disparity1))) {
			Py_DECREF(ret);
			return nullptr;
		}
		// PyTuple_SetItem stole our reference count
		disparity1 = nullptr;

		if (PyTuple_SetItem(ret, 1, reinterpret_cast<PyObject *>(disparity2))) {
			Py_DECREF(ret);
			return nullptr;
		}
		disparity2 = nullptr;

		return ret;
	}

private:
	bool check_buffers()
	{
		if ((input1.format && *input1.format != 'B')
				|| (input2.format && *input2.format != 'B')) {
			PyErr_SetString(PyExc_ValueError,
				"Both the inputs must have 8-bit format");
			return false;
		}
		if (input1.ndim != 2 || input2.ndim != 2) {
			PyErr_SetString(PyExc_ValueError,
				"Both the inputs must be 2D grayscale images");
			return false;
		}
		if (input1.shape[0] != input2.shape[0]
				|| input1.shape[1] != input2.shape[1]) {
			PyErr_SetString(PyExc_ValueError,
				"Inputs must have the same shape");
			return false;
		}
		if (input1.strides[0] != input2.strides[0]) {
			PyErr_SetString(PyExc_ValueError,
				"Inputs must have the same stride");
			return false;
		}
		if (input1.strides[1] > input1.strides[0]) {
			PyErr_SetString(PyExc_ValueError,
				"Buffers must be in C-order (i.e. stored by row)");
			return false;
		}
		return true;
	}

	bool make_output()
	{
		npy_intp shape[] = {input1.shape[0], input1.shape[1]};
		if (self->params.subsampling) {
			shape[0] /= 2;
			shape[1] /= 2;
		}
		disparity1 = reinterpret_cast<PyArrayObject *>(
			PyArray_ZEROS(2, shape, NPY_FLOAT, 0));
		if (!disparity1) {
			return false;
		}
		disparity2 = reinterpret_cast<PyArrayObject *>(
			PyArray_ZEROS(2, shape, NPY_FLOAT, 0));
		if (!disparity2) {
			return false;
		}
		return true;
	}
};

PyObject *Elas_process(ElasObject *self, PyObject *args)
{
	ProcessHelper ph(self);
	return ph.process(args);
}

PyObject *Elas_set_preset(ElasObject *self, PyObject *args)
{
	int preset;
	if (!PyArg_ParseTuple(args, "i", &preset)) {
		return nullptr;
	}

	if (preset != Elas::ROBOTICS && preset != Elas::MIDDLEBURY) {
		PyErr_SetString(PyExc_ValueError, "Invalid preset");
		return nullptr;
	}

	self->params = Elas::parameters(static_cast<Elas::setting>(preset));
	Py_RETURN_NONE;
}

PyMethodDef Elas_methods[] = {
	{"process", reinterpret_cast<PyCFunction>(Elas_process), METH_VARARGS,
		"Matching function.\n"
		"Takes two grayscale images as inputs and returns two float32"
		"numpy arrays.\n"
		"The inputs must be compatible with the buffer protocol."},
	{"set_preset", reinterpret_cast<PyCFunction>(Elas_set_preset), METH_VARARGS,
	 "Set parameters to a preset.\n"
 	 "Available presets are elas.PRESET_ROBOTICS and elas.PRESET_MIDDLEBURY."},
	{nullptr}
};

static PyMemberDef Elas_members[] = {
	{"disp_min", T_INT, offsetof(ElasObject, params.disp_min), 0,
	 "Min disparity"},
	{"disp_max", T_INT, offsetof(ElasObject, params.disp_max), 0,
	 "Max disparity"},
	{"support_threshold", T_FLOAT,
	 offsetof(ElasObject, params.support_threshold), 0,
	 "Max uniqueness ratio (best vs. second best support match)"},
	{"support_texture", T_INT, offsetof(ElasObject, params.support_texture), 0,
	 "Min texture for support points"},
	{"candidate_stepsize", T_INT,
	 offsetof(ElasObject, params.candidate_stepsize), 0,
	 "Step size of regular grid on which support points are matched"},
	{"incon_window_size", T_INT, offsetof(ElasObject, params.incon_window_size),
	 0, "Window size of inconsistent support point check"},
	{"incon_threshold", T_INT, offsetof(ElasObject, params.incon_threshold), 0,
	 "Disparity similarity threshold for support point to be considered "
	 "consistent"},
	{"incon_min_support", T_INT, offsetof(ElasObject, params.incon_min_support),
	 0, "Minimum number of consistent support points"},
	{"add_corners", T_BOOL, offsetof(ElasObject, params.add_corners), 0,
	 "Add support points at image corners with nearest neighbor disparities"},
	{"grid_size", T_INT, offsetof(ElasObject, params.grid_size), 0,
	 "Size of neighborhood for additional support point extrapolation"},
	{"beta", T_FLOAT, offsetof(ElasObject, params.beta), 0,
	 "Image likelihood parameter"},
	{"gamma", T_FLOAT, offsetof(ElasObject, params.gamma), 0,
	 "Prior constant"},
	{"sigma", T_FLOAT, offsetof(ElasObject, params.sigma), 0,
	 "Prior sigma"},
	{"sradius", T_FLOAT, offsetof(ElasObject, params.sradius), 0,
	 "Prior sigma radius"},
	{"match_texture", T_INT, offsetof(ElasObject, params.match_texture), 0,
	 "Min texture for dense matching"},
	{"lr_threshold", T_INT, offsetof(ElasObject, params.lr_threshold), 0,
	 "Disparity threshold for left/right consistency check"},
	{"speckle_sim_threshold", T_FLOAT,
	 offsetof(ElasObject, params.speckle_sim_threshold), 0,
	 "Similarity threshold for speckle segmentation"},
	{"speckle_size", T_INT, offsetof(ElasObject, params.speckle_size), 0,
	 "Maximal size of a speckle (small speckles get removed)"},
	{"ipol_gap_width", T_INT, offsetof(ElasObject, params.ipol_gap_width), 0,
	 "Interpolate small gaps (left<->right, top<->bottom)"},
	{"filter_median", T_BOOL, offsetof(ElasObject, params.filter_median), 0,
	 "Optional median filter (approximated)"},
	{"filter_adaptive_mean", T_BOOL,
	 offsetof(ElasObject, params.filter_adaptive_mean), 0,
	 "Optional adaptive mean filter (approximated)"},
	{"postprocess_only_left", T_BOOL,
	 offsetof(ElasObject, params.postprocess_only_left), 0,
	 "Saves time by not postprocessing the right image"},
	{"subsampling", T_BOOL, offsetof(ElasObject, params.subsampling), 0,
	 "Saves time by only computing disparities for each 2nd pixel"},
	{nullptr}
};

PyTypeObject ElasType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	.tp_name      = "elas.Elas",
	.tp_basicsize = sizeof(ElasObject),
	.tp_itemsize  = 0,
	.tp_flags     = Py_TPFLAGS_DEFAULT,
	.tp_doc       = "The main Elas class",
	.tp_methods   = Elas_methods,
	.tp_members   = Elas_members,
	.tp_init      = reinterpret_cast<initproc>(Elas_init),
	.tp_new       = Elas_new,
};

const char elas_doc[] =
	"These are the bindings for Libelas (LIBrary for Efficient LArge-scale "
	"Stereo matching).";

PyModuleDef elas_module = {
	PyModuleDef_HEAD_INIT, "elas", elas_doc, -1, nullptr};
}

PyMODINIT_FUNC PyInit_elas(void)
{
	PyObject *m = nullptr;

	if(!PyArray_API) {
		import_array();
	}

	if (PyType_Ready(&ElasType) < 0) {
		return nullptr;
	}

	m = PyModule_Create(&elas_module);
	if (!m) {
		return nullptr;
	}

	Py_INCREF(&ElasType);
	if (PyModule_AddObject(m, "Elas",
			reinterpret_cast<PyObject *>(&ElasType)) < 0) {
		Py_DECREF(&ElasType);
		Py_DECREF(m);
		return NULL;
	}

	if (PyModule_AddIntConstant(m, "PRESET_ROBOTICS", Elas::ROBOTICS)
			|| PyModule_AddIntConstant(m, "PRESET_MIDDLEBURY",
			Elas::MIDDLEBURY)) {
		Py_DECREF(&ElasType);
		Py_DECREF(m);
		return nullptr;
	}

	return m;
}
