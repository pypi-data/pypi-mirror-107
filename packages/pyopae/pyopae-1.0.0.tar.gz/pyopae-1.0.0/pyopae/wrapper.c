/* SPDX-License-Identifier: BSD-3-Clause
 * Copyright(c) 2020 Intel Corporation
 */

#include <Python.h>
#include <stdlib.h>
#include <string.h>
#include "opae_api.h"


static PyObject *wrap_version(PyObject *self, PyObject *args)
{
	opae_api_version ver;
	int type = 0;
	char version[OPAE_NAME_SIZE];
	PyObject *d, *v;

	opae_get_api_version(&ver);

	if (PyArg_ParseTuple(args, "|i", &type)) {
		if (type == 0) {
			d = PyDict_New();
			if (d == NULL) {
				opae_log_err("PyDict_New failed\n");
			} else {
				v = Py_BuildValue("I", ver.major);
				PyDict_SetItemString(d, "major", v);
				v = Py_BuildValue("I", ver.minor);
				PyDict_SetItemString(d, "minor", v);
				v = Py_BuildValue("I", ver.micro);
				PyDict_SetItemString(d, "micro", v);
				return d;
			}
		} else {
			snprintf(version, OPAE_NAME_SIZE, "%u.%u.%u",
				ver.major, ver.minor, ver.micro);
			v = Py_BuildValue("s", version);
			return v;
		}
	} else {
		PyErr_Print();
	}

	Py_RETURN_NONE;
}

static PyObject *wrap_set_log_level(PyObject *self, PyObject *args)
{
	int level = -1;
	int ret = -1;

	if (PyArg_ParseTuple(args, "|i", &level))
		ret = opae_set_log_level(level);
	else
		PyErr_Print();

	return Py_BuildValue("i", ret);
}

static PyObject *wrap_set_log_file(PyObject *self, PyObject *args)
{
	char *file = NULL;
	int clean = 0;
	int ret = -1;

	if (PyArg_ParseTuple(args, "|si", &file, &clean))
		ret = opae_set_log_file(file, clean);
	else
		PyErr_Print();

	return Py_BuildValue("i", ret);
}

static PyObject *wrap_get_image_info(PyObject *self, PyObject *args)
{
	char *file = NULL;
	opae_img_info info;
	PyObject *d, *v;

	if (PyArg_ParseTuple(args, "s", &file)) {
		if (opae_get_image_info(file, &info) == 0) {
			d = PyDict_New();
			if (d == NULL) {
				opae_log_err("PyDict_New failed\n");
			} else {
				v = Py_BuildValue("i", info.type);
				PyDict_SetItemString(d, "type", v);
				v = Py_BuildValue("i", info.subtype);
				PyDict_SetItemString(d, "subtype", v);
				v = Py_BuildValue("I", info.total_len);
				PyDict_SetItemString(d, "total_len", v);
				v = Py_BuildValue("I", info.payload_offset);
				PyDict_SetItemString(d, "payload_offset", v);
				v = Py_BuildValue("I", info.payload_len);
				PyDict_SetItemString(d, "payload_len", v);

				return d;
			}
		}
	} else {
		PyErr_Print();
	}
	Py_RETURN_NONE;
}

static PyObject *wrap_proc_type(PyObject *self)
{
	return Py_BuildValue("i", opae_get_proc_type());
}

static PyObject *wrap_init_eal(PyObject *self, PyObject *args)
{
	int argc = 0;
	char **argv;
	int i = 0;
	char *opt = EAL_DEFAULT_OPTIONS;
	char *cmd;
	char *s, *p;
	size_t len = 0;
	int ret = -1;

	if (PyArg_ParseTuple(args, "|s", &opt)) {
		len = strlen(opt);
		if (len > 1024) {
			opae_log_err("EAL parameters is too long\n");
			return Py_BuildValue("i", ret);
		}
		len += strlen(EAL_INIT_FUNCTION) + 2;
		cmd = malloc(len);
		if (cmd == NULL) {
			opae_log_err("malloc failed\n");
		} else {
			snprintf(cmd, len, "%s %s", EAL_INIT_FUNCTION, opt);

			/* count the options */
			s = cmd;
			p = strchr(s, ' ');
			while (p) {
				if (p > s)
					argc++;
				s = p + 1;
				p = strchr(s, ' ');
			}
			if (strlen(s) > 0)
				argc++;

			/* assign option to argv */
			argv = malloc(sizeof(char *) * argc);
			if (argv == NULL) {
				opae_log_err("malloc failed\n");
				free(cmd);
			} else {
				s = cmd;
				p = strchr(s, ' ');
				while (p) {
					if (p > s) {
						argv[i++] = s;
						*p = 0;
					}
					s = p + 1;
					p = strchr(s, ' ');
				}
				if (strlen(s) > 0)
					argv[i++] = s;

				ret = opae_init_eal(argc, argv);
				free(argv);
				free(cmd);
			}
		}
	} else {
		PyErr_Print();
	}
	return Py_BuildValue("i", ret);
}

static PyObject *wrap_cleanup_eal(PyObject *self)
{
	return Py_BuildValue("i", opae_cleanup_eal());
}

static PyObject *wrap_enumerate(PyObject *self, PyObject *args, PyObject *kw)
{
	opae_pci_id filter;
	PyObject *l;
	int i = 0;
	int n = 0;
	opae_pci_device *list = NULL;
	char *kwlist[] = {"vid", "did", "cid", "sub_vid", "sub_did", NULL};

	filter.class_id = BIT_SET_32;
	filter.vendor_id = BIT_SET_16;
	filter.device_id = BIT_SET_16;
	filter.subsystem_vendor_id = BIT_SET_16;
	filter.subsystem_device_id = BIT_SET_16;

	if (PyArg_ParseTupleAndKeywords(args, kw, "|HHIHH", kwlist,
		&filter.vendor_id, &filter.device_id, &filter.class_id,
		&filter.subsystem_vendor_id, &filter.subsystem_device_id)) {
		n = opae_enumerate(&filter, list, 0);
		if (n > 0) {
			if (n > 1024)
				n = 1024;
			list = malloc(n * sizeof(opae_pci_device));
			if (list == NULL)
				opae_log_err("malloc failed\n");
			else
				opae_enumerate(&filter, list, n);
		}

		l = PyList_New(0);
		if (l == NULL) {
			opae_log_err("PyList_New failed\n");
		} else {
			if (list) {
				for (i = 0; i < n; i++)
					PyList_Append(l,
						Py_BuildValue("s",
							list[i].bdf));
				free(list);
			}
			return l;
		}
	} else {
		PyErr_Print();
	}
	Py_RETURN_NONE;
}

static void build_pci_property(PyObject *d, opae_pci_property *p)
{
	PyObject *s, *v;

	s = PyDict_New();
	if (s == NULL) {
		opae_log_err("PyDict_New failed\n");
	} else {
		v = Py_BuildValue("I", p->id.class_id);
		PyDict_SetItemString(s, "class_id", v);
		v = Py_BuildValue("I", p->id.vendor_id);
		PyDict_SetItemString(s, "vendor_id", v);
		v = Py_BuildValue("I", p->id.device_id);
		PyDict_SetItemString(s, "device_id", v);
		v = Py_BuildValue("I", p->id.subsystem_vendor_id);
		PyDict_SetItemString(s, "subsystem_vendor_id", v);
		v = Py_BuildValue("I", p->id.subsystem_device_id);
		PyDict_SetItemString(s, "subsystem_device_id", v);

		PyDict_SetItemString(d, "id", s);
	}

	s = PyDict_New();
	if (s == NULL) {
		opae_log_err("PyDict_New failed\n");
	} else {
		v = Py_BuildValue("I", p->addr.domain);
		PyDict_SetItemString(s, "domain", v);
		v = Py_BuildValue("B", p->addr.bus);
		PyDict_SetItemString(s, "bus", v);
		v = Py_BuildValue("B", p->addr.devid);
		PyDict_SetItemString(s, "device", v);
		v = Py_BuildValue("B", p->addr.function);
		PyDict_SetItemString(s, "function", v);

		PyDict_SetItemString(d, "address", s);
	}

	v = Py_BuildValue("s", p->pci_addr);
	PyDict_SetItemString(d, "bdf", v);
	v = Py_BuildValue("s", p->drv_name);
	PyDict_SetItemString(d, "driver", v);
}

static void build_fme_property(PyObject *d, opae_fme_property *p)
{
	PyObject *v;

	v = Py_BuildValue("I", p->boot_page);
	PyDict_SetItemString(d, "boot_page", v);
	v = Py_BuildValue("I", p->num_ports);
	PyDict_SetItemString(d, "num_ports", v);
	v = Py_BuildValue("K", p->bitstream_id);
	PyDict_SetItemString(d, "bbs_id", v);
	v = Py_BuildValue("K", p->bitstream_metadata);
	PyDict_SetItemString(d, "bbs_metadata", v);
	v = Py_BuildValue("s", p->platform_name);
	PyDict_SetItemString(d, "platform_name", v);
	v = Py_BuildValue("s", p->dcp_version);
	PyDict_SetItemString(d, "dcp_version", v);
	v = Py_BuildValue("s", p->release_name);
	PyDict_SetItemString(d, "release_name", v);
	v = Py_BuildValue("s", p->interface_type);
	PyDict_SetItemString(d, "interface_type", v);
	v = Py_BuildValue("s", p->build_version);
	PyDict_SetItemString(d, "build_version", v);
	v = PyByteArray_FromStringAndSize((const char *)p->pr_id.b, 16);
	PyDict_SetItemString(d, "pr_id", v);
}

static void build_port_property(PyObject *d, opae_port_property *p)
{
	PyObject *v;

	v = PyByteArray_FromStringAndSize(
		(const char *)p->afu_id.b, 16);
	PyDict_SetItemString(d, "afu_id", v);
	v = Py_BuildValue("I", p->type);
	PyDict_SetItemString(d, "type", v);
	v = Py_BuildValue("I", p->index);
	PyDict_SetItemString(d, "index", v);
}

static void build_ports_property(PyObject *d, opae_fpga_property *p)
{
	unsigned int i;
	PyObject *s, *l;

	l = PyList_New(0);
	if (l == NULL) {
		opae_log_err("PyList_New failed\n");
	} else {
		for (i = 0; i < p->fme.num_ports; i++) {
			if (i >= OPAE_MAX_PORT_NUM)
				break;
			s = PyDict_New();
			if (s == NULL) {
				opae_log_err("PyDict_New failed\n");
			} else {
				build_port_property(s, &p->port[i]);
				PyList_Append(l, s);
			}
		}
		PyDict_SetItemString(d, "port", l);
	}
}

static void build_bmc_property(PyObject *d, opae_bmc_property *p)
{
	PyObject *v;

	v = Py_BuildValue("s", p->bmc_version);
	PyDict_SetItemString(d, "bmc_version", v);
	v = Py_BuildValue("s", p->fw_version);
	PyDict_SetItemString(d, "firmware_version", v);
}

static PyObject *wrap_get_property(PyObject *self, PyObject *args)
{
	char *bdf = NULL;
	opae_pci_device fpga;
	unsigned int type = 0;
	opae_fpga_property prop;
	PyObject *d;

	if (PyArg_ParseTuple(args, "s|I", &bdf, &type)) {
		snprintf(fpga.bdf, sizeof(fpga.bdf), "%s", bdf);
		if (opae_get_property(&fpga, &prop, type) == 0) {
			d = PyDict_New();
			if (d == NULL) {
				opae_log_err("PyDict_New failed\n");
			} else {
				if (type == 0)
					type = OPAE_PROP_ALL;

				if (type & OPAE_PROP_PCI)
					build_pci_property(d, &prop.pci);

				if (type & OPAE_PROP_FME)
					build_fme_property(d, &prop.fme);

				if (type & OPAE_PROP_PORT)
					build_ports_property(d, &prop);

				if (type & OPAE_PROP_BMC)
					build_bmc_property(d, &prop.bmc);

				return d;
			}
		}
	} else {
		PyErr_Print();
	}
	Py_RETURN_NONE;
}

static PyObject *wrap_get_phy_info(PyObject *self, PyObject *args)
{
	char *bdf = NULL;
	opae_pci_device fpga;
	opae_phy_info info;
	PyObject *d, *v;

	if (PyArg_ParseTuple(args, "s", &bdf)) {
		snprintf(fpga.bdf, sizeof(fpga.bdf), "%s", bdf);
		if (opae_get_phy_info(&fpga, &info) == 0) {
			d = PyDict_New();
			if (d == NULL) {
				opae_log_err("PyDict_New failed\n");
			} else {
				v = Py_BuildValue("I", info.num_retimers);
				PyDict_SetItemString(d, "num_retimers", v);
				v = Py_BuildValue("I", info.link_speed);
				PyDict_SetItemString(d, "link_speed", v);
				v = Py_BuildValue("I", info.link_status);
				PyDict_SetItemString(d, "link_status", v);

				return d;
			}
		}
	} else {
		PyErr_Print();
	}
	Py_RETURN_NONE;
}

static PyObject *wrap_unbind(PyObject *self, PyObject *args)
{
	char *bdf = NULL;
	opae_pci_device fpga;
	int ret = -1;

	if (PyArg_ParseTuple(args, "s", &bdf)) {
		snprintf(fpga.bdf, sizeof(fpga.bdf), "%s", bdf);
		ret = opae_unbind_driver(&fpga);
	} else {
		PyErr_Print();
	}
	return Py_BuildValue("i", ret);
}

static PyObject *wrap_bind(PyObject *self, PyObject *args)
{
	char *bdf = NULL;
	opae_pci_device fpga;
	char *drv = NULL;
	int ret = -1;

	if (PyArg_ParseTuple(args, "ss", &bdf, &drv)) {
		snprintf(fpga.bdf, sizeof(fpga.bdf), "%s", bdf);
		ret = opae_bind_driver(&fpga, drv);
	} else {
		PyErr_Print();
	}
	return Py_BuildValue("i", ret);
}

static PyObject *wrap_remove(PyObject *self, PyObject *args)
{
	char *bdf = NULL;
	opae_pci_device fpga;
	int ret = -1;

	if (PyArg_ParseTuple(args, "s", &bdf)) {
		snprintf(fpga.bdf, sizeof(fpga.bdf), "%s", bdf);
		ret = opae_remove_device(&fpga);
	} else {
		PyErr_Print();
	}
	return Py_BuildValue("i", ret);
}

static PyObject *wrap_probe(PyObject *self, PyObject *args)
{
	char *bdf = NULL;
	opae_pci_device fpga;
	int ret = -1;

	if (PyArg_ParseTuple(args, "s", &bdf)) {
		snprintf(fpga.bdf, sizeof(fpga.bdf), "%s", bdf);
		ret = opae_probe_device(&fpga);
	} else {
		PyErr_Print();
	}
	return Py_BuildValue("i", ret);
}

static PyObject *wrap_get_parent(PyObject *self, PyObject *args)
{
	char *bdf = NULL;
	opae_pci_device fpga;
	opae_pci_device parent;
	int ret = 0;

	if (PyArg_ParseTuple(args, "s", &bdf)) {
		snprintf(fpga.bdf, sizeof(fpga.bdf), "%s", bdf);
		ret = opae_get_parent(&fpga, &parent);
		if (ret > 0)
			return Py_BuildValue("s", parent.bdf);
	} else {
		PyErr_Print();
	}
	Py_RETURN_NONE;
}

static PyObject *wrap_get_child(PyObject *self, PyObject *args)
{
	char *bdf = NULL;
	opae_pci_device fpga;
	opae_pci_device *list = NULL;
	PyObject *l;
	int i = 0;
	int n = 0;

	if (PyArg_ParseTuple(args, "s", &bdf)) {
		snprintf(fpga.bdf, sizeof(fpga.bdf), "%s", bdf);
		n = opae_get_child(&fpga, list, 0);
		if (n > 0) {
			if (n > 1024)
				n = 1024;
			list = malloc(n * sizeof(opae_pci_device));
			if (list == NULL)
				opae_log_err("malloc failed\n");
			else
				opae_get_child(&fpga, list, n);
		}

		l = PyList_New(0);
		if (l == NULL) {
			opae_log_err("PyList_New failed\n");
		} else {
			if (list) {
				for (i = 0; i < n; i++)
					PyList_Append(l, Py_BuildValue("s",
						list[i].bdf));
				free(list);
			}
			return l;
		}
	} else {
		PyErr_Print();
	}
	Py_RETURN_NONE;
}

static PyObject *wrap_get_pf1(PyObject *self, PyObject *args)
{
	char *bdf = NULL;
	opae_pci_device fpga;
	opae_pci_device *list = NULL;
	PyObject *l;
	int i = 0;
	int n = 0;

	if (PyArg_ParseTuple(args, "s", &bdf)) {
		snprintf(fpga.bdf, sizeof(fpga.bdf), "%s", bdf);
		n = opae_get_pf1(&fpga, list, 0);
		if (n > 0) {
			if (n > 1024)
				n = 1024;
			list = malloc(n * sizeof(opae_pci_device));
			if (list == NULL)
				opae_log_err("malloc failed\n");
			else
				opae_get_pf1(&fpga, list, n);
		}

		l = PyList_New(0);
		if (l == NULL) {
			opae_log_err("PyList_New failed\n");
		} else {
			if (list) {
				for (i = 0; i < n; i++)
					PyList_Append(l, Py_BuildValue("s",
						list[i].bdf));
				free(list);
			}
			return l;
		}
	} else {
		PyErr_Print();
	}
	Py_RETURN_NONE;
}

static PyObject *wrap_set_status(PyObject *self, PyObject *args)
{
	char *bdf = NULL;
	opae_pci_device fpga;
	uint32_t status = 0;
	uint32_t progress = 0;
	int ret = -1;

	if (PyArg_ParseTuple(args, "s|ii", &bdf, &status, &progress)) {
		snprintf(fpga.bdf, sizeof(fpga.bdf), "%s", bdf);
		ret = opae_store_rsu_status(&fpga, status, progress);
	} else {
		PyErr_Print();
	}
	return Py_BuildValue("i", ret);
}

static PyObject *wrap_get_status(PyObject *self, PyObject *args)
{
	char *bdf = NULL;
	opae_pci_device fpga;
	uint32_t status = 0;
	uint32_t progress = 0;
	int ret = 0;
	PyObject *d, *v;

	if (PyArg_ParseTuple(args, "s", &bdf)) {
		snprintf(fpga.bdf, sizeof(fpga.bdf), "%s", bdf);
		ret = opae_load_rsu_status(&fpga, &status, &progress);
		if (ret == 0) {
			d = PyDict_New();
			if (d == NULL) {
				opae_log_err("PyDict_New failed\n");
			} else {
				v = Py_BuildValue("I", status);
				PyDict_SetItemString(d, "status", v);
				v = Py_BuildValue("I", progress);
				PyDict_SetItemString(d, "progress", v);
				return d;
			}
		}
	} else {
		PyErr_Print();
	}
	Py_RETURN_NONE;
}

static PyObject *wrap_flash(PyObject *self, PyObject *args, PyObject *kw)
{
	char *bdf = NULL;
	opae_pci_device fpga;
	char *file = NULL;
	uint64_t status = 0;
	int ret = -1;
	char *kwlist[] = {"id", "file", NULL};

	if (PyArg_ParseTupleAndKeywords(args, kw, "ss|", kwlist, &bdf, &file)) {
		snprintf(fpga.bdf, sizeof(fpga.bdf), "%s", bdf);
		Py_BEGIN_ALLOW_THREADS
		ret = opae_update_flash(&fpga, file, &status);
		Py_END_ALLOW_THREADS
	} else {
		PyErr_Print();
	}
	return Py_BuildValue("i", ret);
}

static PyObject *wrap_cancel(PyObject *self, PyObject *args)
{
	char *bdf = NULL;
	opae_pci_device fpga;
	int force = 0;
	int ret = -1;

	if (PyArg_ParseTuple(args, "s|i", &bdf, &force)) {
		snprintf(fpga.bdf, sizeof(fpga.bdf), "%s", bdf);
		ret = opae_cancel_flash_update(&fpga, force);
	} else {
		PyErr_Print();
	}
	return Py_BuildValue("i", ret);
}

static PyObject *wrap_reboot(PyObject *self, PyObject *args, PyObject *kw)
{
	char *bdf = NULL;
	opae_pci_device fpga;
	int type = 0;
	int page = 1;
	int ret = -1;
	char *kwlist[] = {"id", "type", "page", NULL};

	if (PyArg_ParseTupleAndKeywords(args, kw, "s|ii", kwlist,
		&bdf, &type, &page)) {
		snprintf(fpga.bdf, sizeof(fpga.bdf), "%s", bdf);
		ret = opae_reboot_device(&fpga, type, page);
	} else {
		PyErr_Print();
	}
	return Py_BuildValue("i", ret);
}

static PyObject *wrap_pr(PyObject *self, PyObject *args, PyObject *kw)
{
	char *bdf = NULL;
	opae_pci_device fpga;
	int port = 0;
	char *file = NULL;
	int ret = -1;
	char *kwlist[] = {"id", "port", "file", NULL};

	if (PyArg_ParseTupleAndKeywords(args, kw, "sis|", kwlist,
		&bdf, &port, &file)) {
		snprintf(fpga.bdf, sizeof(fpga.bdf), "%s", bdf);
		ret = opae_partial_reconfigure(&fpga, port, file);
	} else {
		PyErr_Print();
	}
	return Py_BuildValue("i", ret);
}

static PyObject *wrap_pci_read(PyObject *self, PyObject *args, PyObject *kw)
{
	char *bdf = NULL;
	opae_pci_device fpga;
	uint32_t addr = 0;
	uint32_t val = 0;
	int ret = 0;
	char *kwlist[] = {"id", "addr", NULL};

	if (PyArg_ParseTupleAndKeywords(args, kw, "sI", kwlist, &bdf, &addr)) {
		snprintf(fpga.bdf, sizeof(fpga.bdf), "%s", bdf);
		ret = opae_read_pci_cfg(&fpga, addr, &val);
		if (ret == 0)
			return Py_BuildValue("I", val);
	} else {
		PyErr_Print();
	}
	Py_RETURN_NONE;
}

static PyObject *wrap_pci_write(PyObject *self, PyObject *args, PyObject *kw)
{
	char *bdf = NULL;
	opae_pci_device fpga;
	uint32_t addr = 0;
	uint64_t val = 0;
	int ret = 0;
	char *kwlist[] = {"id", "addr", "val", NULL};

	if (PyArg_ParseTupleAndKeywords(args, kw, "sII", kwlist,
		&bdf, &addr, &val)) {
		snprintf(fpga.bdf, sizeof(fpga.bdf), "%s", bdf);
		ret = opae_write_pci_cfg(&fpga, addr, val);
		if (ret == 0)
			return Py_BuildValue("I", val);
	} else {
		PyErr_Print();
	}
	Py_RETURN_NONE;
}


static PyMethodDef opaeAPIs[] = {
	{"get_api_version", (PyCFunction)wrap_version, METH_VARARGS,
	 "Get API's version"},
	{"set_log_level", (PyCFunction)wrap_set_log_level, METH_VARARGS,
	 "Set API's log level"},
	{"set_log_file", (PyCFunction)wrap_set_log_file, METH_VARARGS,
	 "Set API's log file"},
	{"get_image_info", (PyCFunction)wrap_get_image_info, METH_VARARGS,
	 "Get information of the bitstream image file"},
	{"get_proc_type", (PyCFunction)wrap_proc_type, METH_NOARGS,
	 "Get DPDK process type"},
	{"init_eal", (PyCFunction)wrap_init_eal, METH_VARARGS,
	 "Initialize EAL environment"},
	{"cleanup_eal", (PyCFunction)wrap_cleanup_eal, METH_NOARGS,
	 "Cleanup EAL environment"},
	{"enumerate", (PyCFunction)wrap_enumerate, METH_VARARGS | METH_KEYWORDS,
	 "Enumerate specified PCI device"},
	{"get_property", (PyCFunction)wrap_get_property, METH_VARARGS,
	 "Get property of specified PCI device"},
	{"get_phy_info", (PyCFunction)wrap_get_phy_info, METH_VARARGS,
	 "Get information of PHY device"},
	{"unbind", (PyCFunction)wrap_unbind, METH_VARARGS,
	 "Unbind specified PCI device from driver"},
	{"bind", (PyCFunction)wrap_bind, METH_VARARGS,
	 "Bind specified PCI device to driver"},
	{"remove", (PyCFunction)wrap_remove, METH_VARARGS,
	 "Remove specified PCI device from DPDK"},
	{"probe", (PyCFunction)wrap_probe, METH_VARARGS,
	 "Probe specified PCI device to DPDK"},
	{"get_parent", (PyCFunction)wrap_get_parent, METH_VARARGS,
	 "Get parent of specified PCI device"},
	{"get_child", (PyCFunction)wrap_get_child, METH_VARARGS,
	 "Get child of specified PCI device"},
	{"get_pf1", (PyCFunction)wrap_get_pf1, METH_VARARGS,
	 "Get the second physical function of specified PCI device"},
	{"set_status", (PyCFunction)wrap_set_status, METH_VARARGS,
	 "Set status of specified PCI device"},
	{"get_status", (PyCFunction)wrap_get_status, METH_VARARGS,
	 "Get status of specified PCI device"},
	{"flash", (PyCFunction)wrap_flash, METH_VARARGS | METH_KEYWORDS,
	 "Write bitstream into flash of specified PCI device"},
	{"cancel", (PyCFunction)wrap_cancel, METH_VARARGS,
	 "Cancel flash update progress on specified PCI device"},
	{"reboot", (PyCFunction)wrap_reboot, METH_VARARGS | METH_KEYWORDS,
	 "Reboot specified PCI device"},
	{"pr", (PyCFunction)wrap_pr, METH_VARARGS | METH_KEYWORDS,
	 "Partial reload AFU in specified port"},
	{"pci_read", (PyCFunction)wrap_pci_read, METH_VARARGS | METH_KEYWORDS,
	 "Read from configuration space of specified PCI device"},
	{"pci_write", (PyCFunction)wrap_pci_write, METH_VARARGS | METH_KEYWORDS,
	 "Write to configuration space of specified PCI device"},
	{NULL, NULL, 0, NULL}
};

static struct PyModuleDef fpgamodule = {
	PyModuleDef_HEAD_INIT, "fpga", "OPAE Python API", -1, opaeAPIs
};

PyMODINIT_FUNC PyInit_fpga(void)
{
	return PyModule_Create(&fpgamodule);
}
