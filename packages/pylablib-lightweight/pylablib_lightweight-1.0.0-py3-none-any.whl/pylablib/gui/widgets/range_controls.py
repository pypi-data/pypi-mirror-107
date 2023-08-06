from ...core.gui import QtCore, QtWidgets, Signal

from ...core.gui.widgets.edit import NumEdit
from ...core.utils.numerical import limit_to_range

import collections




##### Range control #####

class RangeCtl(QtWidgets.QWidget):
    """
    Class for range control.

    Can have any subset of 3 rows: specifying min-max, specifying center-span (connected to min-max), and specifying step.

    Like most widgets, requires calling :meth:`setupUi` to set up before usage.

    Args:
        parent: parent widget

    Signals:
        - ``value_changed``: emitted when the value is changed
    """
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self,parent)

    def setupUi(self, name, lim=(None,None), order=True, formatter="float", labels=("Min","Max","Center","Span","Step"), elements=("minmax","cspan","step")):
        """
        Setup the range control.

        Args:
            name (str): widget name
            lim (tuple): limit containing min and max values
            order (bool): if ``True``, first value is always smaller than the second one (values are swapped otherwise)
            formatter (str): formatter for all edit boxes; see :func:`.format.as_formatter` for details
            labels (tuple): tuple of 5 labels for 5 controls: min, max, center, span, and step (need to always specify 5, even if no all elements are included)
            elements (tuple): tuple specifying elements which are displayed for the control;
                can contain ``"minmax"`` (min-max row), ``"cspan"`` (center-span row), and ``"step"`` (step row)
        """
        self.name=name
        self.order=order
        self.rng=(0,0,0) if "step" in elements else (0,0)
        self.setObjectName(self.name)
        self.gridLayout=QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        row=0
        if "minmax" in elements:
            self.labelMin=QtWidgets.QLabel(self)
            self.labelMin.setObjectName("labelMin")
            self.labelMin.setText(labels[0])
            self.gridLayout.addWidget(self.labelMin, row, 0, 1, 1)
            self.labelMax=QtWidgets.QLabel(self)
            self.labelMax.setObjectName("labelMax")
            self.labelMax.setText(labels[1])
            self.gridLayout.addWidget(self.labelMax, row, 2, 1, 1)
            self.e_min=NumEdit(self)
            self.e_min.setObjectName("e_min")
            self.gridLayout.addWidget(self.e_min, row, 1, 1, 1)
            self.e_max=NumEdit(self)
            self.e_max.setObjectName("e_max")
            self.gridLayout.addWidget(self.e_max, row, 3, 1, 1)
            self.e_min.value_changed.connect(self._minmax_changed)
            self.e_max.value_changed.connect(self._minmax_changed)
            row+=1
        else:
            self.e_min=None
            self.e_max=None
        if "cspan" in elements:
            self.labelCent=QtWidgets.QLabel(self)
            self.labelCent.setObjectName("labelCent")
            self.labelCent.setText(labels[2])
            self.gridLayout.addWidget(self.labelCent, row, 0, 1, 1)
            self.labelSpan=QtWidgets.QLabel(self)
            self.labelSpan.setObjectName("labelSpan")
            self.labelSpan.setText(labels[3])
            self.gridLayout.addWidget(self.labelSpan, row, 2, 1, 1)
            self.e_cent=NumEdit(self)
            self.e_cent.setObjectName("e_cent")
            self.gridLayout.addWidget(self.e_cent, row, 1, 1, 1)
            self.e_span=NumEdit(self)
            self.e_span.setObjectName("e_span")
            self.gridLayout.addWidget(self.e_span, row, 3, 1, 1)
            self.e_cent.value_changed.connect(self._cspan_changed)
            self.e_span.value_changed.connect(self._cspan_changed)
            row+=1
        else:
            self.e_cent=None
            self.e_span=None
        if "step" in elements:
            self.labelStep=QtWidgets.QLabel(self)
            self.labelStep.setObjectName("labelStep")
            self.labelStep.setText(labels[4])
            self.gridLayout.addWidget(self.labelStep, row, 0, 1, 1)
            self.e_step=NumEdit(self)
            self.e_step.setObjectName("e_step")
            self.gridLayout.addWidget(self.e_step, row, 1, 1, 1)
            self.e_step.value_changed.connect(self._step_changed)
            self.e_step.set_limiter((0,None))
            row+=1
        else:
            self.e_step=None
        self.gridLayout.setContentsMargins(2,2,2,2)
        for v in [self.e_min,self.e_max,self.e_cent,self.e_span,self.e_step]:
            if v:
                v.change_formatter(formatter)
        self._show_values(self.rng)
        self.set_limit(lim)

    def _limit_range(self, rng):
        vmin=limit_to_range(rng[0],*self.lim)
        vmax=limit_to_range(rng[1],*self.lim)
        if self.order:
            vmin,vmax=min(vmin,vmax),max(vmin,vmax)
        if self.e_step is None:
            return (vmin,vmax)
        else:
            step=max(0,rng[2]) if len(rng)>2 else 0
            return (vmin,vmax,step)
    def _minmax_changed(self):
        rng=(self.e_min.get_value(),self.e_max.get_value())+self.rng[2:]
        self.set_value(rng)
    def _cspan_changed(self):
        cent,span=self.e_cent.get_value(),self.e_span.get_value()
        rng=((cent-span/2.),(cent+span/2.))+self.rng[2:]
        self.set_value(rng)
    def _step_changed(self):
        rng=self.rng[0],self.rng[1],self.e_step.get_value()
        self.set_value(rng)

    def set_limit(self, lim):
        """Set range values limit (2-tuple)"""
        self.lim=lim
        self.set_value(self.rng)

    value_changed=Signal(object)
    def get_value(self):
        """Get current range value (3-tuple ``(left, right, step)`` if step is included, or 2-tuple ``(left, right)`` if it's not)"""
        return self.rng
    def _show_values(self, rng):
        if self.e_min:
            self.e_min.set_value(rng[0],notify_value_change=False)
            self.e_max.set_value(rng[1],notify_value_change=False)
        if self.e_cent:
            self.e_cent.set_value((rng[0]+rng[1])/2.,notify_value_change=False)
            self.e_span.set_value(rng[1]-rng[0],notify_value_change=False)
        if self.e_step:
            self.e_step.set_value(rng[2],notify_value_change=False)
    def set_value(self, rng, notify_value_change=True):
        """
        Get current range value
        
        `rng` is a 2-tuple ``(left, right)``
        If ``notify_value_change==True``, emit the `value_changed` signal; otherwise, change value silently.
        """
        rng=self._limit_range(rng)
        if self.rng!=rng:
            self.rng=rng
            self._show_values(rng)
            if notify_value_change:
                self.value_changed.emit(rng)







##### ROI control #####


TAxisParams=collections.namedtuple("AxisParams",["min","max"])
class ROICtl(QtWidgets.QWidget):
    """
    Class for ROI control.

    Has 2 rows (for X and Y coordinates), each with 2 numerical edits: min and max (or width, depending on :func:`setupUi` parameters).

    Like most widgets, requires calling :meth:`setupUi` to set up before usage.

    Args:
        parent: parent widget

    Attributes:
        value_changed: signal emitted when the ROI value is changed
    """
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        self.xparams=TAxisParams(0,1)
        self.yparams=TAxisParams(0,1)
        self.validate=None
        self.xlim=(0,None)
        self.ylim=(0,None)
        self.minsize=0

    def _limit_range(self, rng, lim, minsize, maxsize):
        vmin=limit_to_range(rng.min,*lim)
        vmax=limit_to_range(rng.max,*lim)
        vmin,vmax=min(vmin,vmax),max(vmin,vmax)
        if vmax-vmin<minsize: # try increase upper limit
            vmax=limit_to_range(vmin+minsize,*lim)
        if vmax-vmin<minsize: # try decrease lower limit
            vmin=limit_to_range(vmax-minsize,*lim)
        if maxsize and (vmax-vmin>minsize):
            vmax=vmin+maxsize
        return TAxisParams(int(vmin),int(vmax))
    def validateROI(self, xparams, yparams):
        """Restrict current ROI values according to the class constraints"""
        xminsize,yminsize=self.minsize if isinstance(self.minsize,tuple) else (self.minsize,self.minsize)
        xmaxsize,ymaxsize=self.maxsize if isinstance(self.maxsize,tuple) else (self.maxsize,self.maxsize)
        xparams=self._limit_range(xparams,self.xlim,xminsize,xmaxsize)
        yparams=self._limit_range(yparams,self.ylim,yminsize,ymaxsize)
        if self.validate:
            xparams,yparams=self.validate((xparams,yparams))
            xparams=TAxisParams(*xparams)
            yparams=TAxisParams(*yparams)
        return xparams,yparams
    def setupUi(self, name, xlim=(0,None), ylim=None, minsize=0, maxsize=None, labels=("X","Y"), kind="minmax", validate=None):
        """
        Setup the ROI control.

        Args:
            name (str): widget name
            xlim (tuple): limit for x-axis min and max values
            ylim (tuple): limit for y-axis min and max values
            sizelim (int or tuple): minimal allowed size (int implies same for both axes)
            maxsize (int or tuple): maximal allowed size (int implies same for both axes)
            kind (str): can be either ``"minmax"`` (each axis control are min, max, and bin) or ``"minsize"`` (each axis control are min, size and bin)
            validate: if not ``None``, a function which takes tuple ``(xparams, yparams)`` of two axes parameters (each is a 3-tuple ``(min, max, bin)``)
                and return their constrained versions.
        """
        self.name=name
        self.kind=kind
        self.setObjectName(self.name)
        self.setMinimumSize(QtCore.QSize(100,60))
        self.setMaximumSize(QtCore.QSize(2**16,60))
        self.gridLayout=QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.labelROI=QtWidgets.QLabel(self)
        self.labelROI.setObjectName("labelROI")
        self.labelROI.setText("ROI")
        self.gridLayout.addWidget(self.labelROI,0,0,1,1)
        self.labelMin=QtWidgets.QLabel(self)
        self.labelMin.setObjectName("labelMin")
        self.labelMin.setText("Min")
        self.gridLayout.addWidget(self.labelMin,0,1,1,1)
        self.labelMax=QtWidgets.QLabel(self)
        self.labelMax.setObjectName("labelMax")
        self.labelMax.setText("Max" if kind=="minmax" else "Size")
        self.gridLayout.addWidget(self.labelMax,0,2,1,1)
        self.labelX=QtWidgets.QLabel(self)
        self.labelX.setObjectName("labelX")
        self.labelX.setText(labels[0])
        self.gridLayout.addWidget(self.labelX,1,0,1,1)
        self.labelY=QtWidgets.QLabel(self)
        self.labelY.setObjectName("labelY")
        self.labelY.setText(labels[1])
        self.gridLayout.addWidget(self.labelY,2,0,1,1)
        self.x_min=NumEdit(self)
        self.x_min.setObjectName("x_min")
        self.gridLayout.addWidget(self.x_min,1,1,1,1)
        self.x_max=NumEdit(self)
        self.x_max.setObjectName("x_max")
        self.gridLayout.addWidget(self.x_max,1,2,1,1)
        self.y_min=NumEdit(self)
        self.y_min.setObjectName("y_min")
        self.gridLayout.addWidget(self.y_min,2,1,1,1)
        self.y_max=NumEdit(self)
        self.y_max.setObjectName("y_max")
        self.gridLayout.addWidget(self.y_max,2,2,1,1)
        self.gridLayout.setContentsMargins(0,0,0,0)
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Preferred))
        self.gridLayout.setSpacing(4)
        self.gridLayout.setColumnStretch(1,2)
        self.gridLayout.setColumnStretch(2,2)
        self.validate=validate
        for v in [self.x_min,self.y_min]:
            v.set_formatter("int")
            v.set_limiter((None,None,"coerce","int"))
            v.set_value(0)
        for v in [self.x_max,self.x_bin,self.y_max]:
            v.set_formatter("int")
            v.set_limiter((None,None,"coerce","int"))
            v.set_value(1)
        for v in [self.x_min,self.x_max,self.x_bin,self.y_min,self.y_max]:
            v.setMinimumWidth(40)
            v.value_changed.connect(self._on_edit)
        self.set_limits(xlim,ylim,minsize=minsize,maxsize=maxsize)


    def set_limits(self, xlim="keep", ylim="keep", minsize="keep", maxsize="keep"):
        """
        Set limits for various parameters.

        If value is ``"keep"``, keep the current value; if value is ``None``, impose no constraints.
        `maxbin`, `minsize` and `maxsize` can be integers or 2-tuples depending on whether the limits are the same or different for two axes.
        """
        if xlim!="keep":
            self.xlim=xlim
        if ylim!="keep":
            self.ylim=ylim or xlim
        if minsize!="keep":
            self.minsize=minsize
        if maxsize!="keep":
            self.maxsize=maxsize
        for v in [self.x_min,self.x_max]:
            v.set_limiter((self.xlim[0],self.xlim[1],"coerce","int"))
        for v in [self.y_min,self.y_max]:
            v.set_limiter((self.ylim[0],self.ylim[1],"coerce","int"))
        for v in [self.x_bin,self.y_bin]:
            v.set_limiter((1,self.maxbin,"coerce","int"))
        self._show_values(*self.get_value())

    value_changed=Signal(object)
    def _on_edit(self):
        params=self.get_value()
        self._show_values(*params)
        self.value_changed.emit(params)

    def get_value(self):
        """
        Get ROI value.

        Return tuple ``(xparams, yparams)`` of two axes parameters (each is a 2-tuple ``(min, max)``).
        """
        if self.kind=="minmax":
            xparams=TAxisParams(self.x_min.get_value(),self.x_max.get_value())
            yparams=TAxisParams(self.y_min.get_value(),self.y_max.get_value())
        else:
            xmin=self.x_min.get_value()
            ymin=self.y_min.get_value()
            xparams=TAxisParams(xmin,xmin+self.x_max.get_value())
            yparams=TAxisParams(ymin,ymin+self.y_max.get_value())
        return self.validateROI(xparams,yparams)
    def _show_values(self, xparams, yparams):
        if self.kind=="minmax":
            xmax,ymax=xparams.max,yparams.max
        else:
            xmax,ymax=xparams.max-xparams.min,yparams.max-yparams.min
        self.x_min.set_value(xparams.min,notify_value_change=False)
        self.x_max.set_value(xmax,notify_value_change=False)
        self.y_min.set_value(yparams.min,notify_value_change=False)
        self.y_max.set_value(ymax,notify_value_change=False)
    def set_value(self, roi, notify_value_change=True):
        """
        Set ROI value.

        `roi` is a tuple ``(xparams, yparams)`` of two axes parameters (each is a 2-tuple ``(min, max)``).
        If ``notify_value_change==True``, emit the `value_changed` signal; otherwise, change value silently.
        """
        roi=TAxisParams(*roi[0]),TAxisParams(*roi[1])
        params=self.validateROI(*roi)
        self._show_values(*params)
        if notify_value_change:
            self.value_changed.emit(params)




TBinAxisParams=collections.namedtuple("TBinAxisParams",["min","max","bin"])
class BinROICtl(ROICtl):
    """
    Class for ROI control with binning.

    Has 2 rows (for X and Y coordinates), each with 3 numerical edits: min, max (or width, depending on :func:`setupUi` parameters), and bin.

    Like most widgets, requires calling :meth:`setupUi` to set up before usage.

    Args:
        parent: parent widget

    Attributes:
        value_changed: signal emitted when the ROI value is changed
    """
    def __init__(self, parent=None):
        ROICtl.__init__(self,parent)
        self.xparams=TBinAxisParams(0,1,1)
        self.yparams=TBinAxisParams(0,1,1)
        self.maxbin=None

    def _limit_range(self, rng, lim, maxbin, minsize, maxsize):
        vmin=limit_to_range(rng.min,*lim)
        vmax=limit_to_range(rng.max,*lim)
        vmin,vmax=min(vmin,vmax),max(vmin,vmax)
        if vmax-vmin<minsize: # try increase upper limit
            vmax=limit_to_range(vmin+minsize,*lim)
        if vmax-vmin<minsize: # try decrease lower limit
            vmin=limit_to_range(vmax-minsize,*lim)
        if maxsize and (vmax-vmin>minsize):
            vmax=vmin+maxsize
        vbin=limit_to_range(rng.bin,1,maxbin)
        return TBinAxisParams(int(vmin),int(vmax),int(vbin))
    def validateROI(self, xparams, yparams):
        """Restrict current ROI values according to the class constraints"""
        xminsize,yminsize=self.minsize if isinstance(self.minsize,tuple) else (self.minsize,self.minsize)
        xmaxsize,ymaxsize=self.maxsize if isinstance(self.maxsize,tuple) else (self.maxsize,self.maxsize)
        xparams=self._limit_range(xparams,self.xlim,self.maxbin,xminsize,xmaxsize)
        yparams=self._limit_range(yparams,self.ylim,self.maxbin,yminsize,ymaxsize)
        if self.validate:
            xparams,yparams=self.validate((xparams,yparams))
            xparams=TBinAxisParams(*xparams)
            yparams=TBinAxisParams(*yparams)
        return xparams,yparams
    def setupUi(self, name, xlim=(0,None), ylim=None, maxbin=None, minsize=0, maxsize=None, kind="minmax", validate=None):
        """
        Setup the ROI control.

        Args:
            name (str): widget name
            xlim (tuple): limit for x-axis min and max values
            ylim (tuple): limit for y-axis min and max values
            maxbin (int or tuple): maximal allowed binning (int implies same for both axes)
            minsize (int or tuple): minimal allowed size (int implies same for both axes)
            maxsize (int or tuple): maximal allowed size (int implies same for both axes)
            kind (str): can be either ``"minmax"`` (each axis control are min, max, and bin) or ``"minsize"`` (each axis control are min, size and bin)
            validate: if not ``None``, a function which takes tuple ``(xparams, yparams)`` of two axes parameters (each is a 3-tuple ``(min, max, bin)``)
                and return their constrained versions.
        """
        self.name=name
        self.kind=kind
        self.setObjectName(self.name)
        self.setMinimumSize(QtCore.QSize(100,60))
        self.setMaximumSize(QtCore.QSize(2**16,60))
        self.gridLayout=QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.labelROI=QtWidgets.QLabel(self)
        self.labelROI.setObjectName("labelROI")
        self.labelROI.setText("ROI")
        self.gridLayout.addWidget(self.labelROI,0,0,1,1)
        self.labelMin=QtWidgets.QLabel(self)
        self.labelMin.setObjectName("labelMin")
        self.labelMin.setText("Min")
        self.gridLayout.addWidget(self.labelMin,0,1,1,1)
        self.labelMax=QtWidgets.QLabel(self)
        self.labelMax.setObjectName("labelMax")
        self.labelMax.setText("Max" if kind=="minmax" else "Size")
        self.gridLayout.addWidget(self.labelMax,0,2,1,1)
        self.labelBin=QtWidgets.QLabel(self)
        self.labelBin.setObjectName("labelBin")
        self.labelBin.setText("Bin")
        self.gridLayout.addWidget(self.labelBin,0,3,1,1)
        self.labelX=QtWidgets.QLabel(self)
        self.labelX.setObjectName("labelX")
        self.labelX.setText("X")
        self.gridLayout.addWidget(self.labelX,1,0,1,1)
        self.labelY=QtWidgets.QLabel(self)
        self.labelY.setObjectName("labelY")
        self.labelY.setText("Y")
        self.gridLayout.addWidget(self.labelY,2,0,1,1)
        self.x_min=NumEdit(self)
        self.x_min.setObjectName("x_min")
        self.gridLayout.addWidget(self.x_min,1,1,1,1)
        self.x_max=NumEdit(self)
        self.x_max.setObjectName("x_max")
        self.gridLayout.addWidget(self.x_max,1,2,1,1)
        self.x_bin=NumEdit(self)
        self.x_bin.setObjectName("x_bin")
        self.gridLayout.addWidget(self.x_bin,1,3,1,1)
        self.y_min=NumEdit(self)
        self.y_min.setObjectName("y_min")
        self.gridLayout.addWidget(self.y_min,2,1,1,1)
        self.y_max=NumEdit(self)
        self.y_max.setObjectName("y_max")
        self.gridLayout.addWidget(self.y_max,2,2,1,1)
        self.y_bin=NumEdit(self)
        self.y_bin.setObjectName("y_bin")
        self.gridLayout.addWidget(self.y_bin,2,3,1,1)
        self.gridLayout.setContentsMargins(0,0,0,0)
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Preferred))
        self.gridLayout.setSpacing(4)
        self.gridLayout.setColumnStretch(1,2)
        self.gridLayout.setColumnStretch(2,2)
        self.gridLayout.setColumnStretch(3,1)
        self.validate=validate
        for v in [self.x_min,self.y_min]:
            v.set_formatter("int")
            v.set_limiter((None,None,"coerce","int"))
            v.set_value(0)
        for v in [self.x_max,self.x_bin,self.y_max,self.y_bin]:
            v.set_formatter("int")
            v.set_limiter((None,None,"coerce","int"))
            v.set_value(1)
        for v in [self.x_min,self.x_max,self.x_bin,self.y_min,self.y_max,self.y_bin]:
            v.setMinimumWidth(40)
            v.value_changed.connect(self._on_edit)
        self.set_limits(xlim,ylim,maxbin=maxbin,minsize=minsize,maxsize=maxsize)


    def set_limits(self, xlim="keep", ylim="keep", maxbin="keep", minsize="keep", maxsize="keep"):
        """
        Set limits for various parameters.

        If value is ``"keep"``, keep the current value; if value is ``None``, impose no constraints.
        `maxbin`, `minsize` and `maxsize` can be integers or 2-tuples depending on whether the limits are the same or different for two axes.
        """
        if xlim!="keep":
            self.xlim=xlim
        if ylim!="keep":
            self.ylim=ylim or xlim
        if maxbin!="keep":
            self.maxbin=maxbin
        if minsize!="keep":
            self.minsize=minsize
        if maxsize!="keep":
            self.maxsize=maxsize
        for v in [self.x_min,self.x_max]:
            v.set_limiter((self.xlim[0],self.xlim[1],"coerce","int"))
        for v in [self.y_min,self.y_max]:
            v.set_limiter((self.ylim[0],self.ylim[1],"coerce","int"))
        for v in [self.x_bin,self.y_bin]:
            v.set_limiter((1,self.maxbin,"coerce","int"))
        self._show_values(*self.get_value())

    def get_value(self):
        """
        Get ROI value.

        Return tuple ``(xparams, yparams)`` of two axes parameters (each is a 3-tuple ``(min, max, bin)``).
        """
        if self.kind=="minmax":
            xparams=TBinAxisParams(self.x_min.get_value(),self.x_max.get_value(),self.x_bin.get_value())
            yparams=TBinAxisParams(self.y_min.get_value(),self.y_max.get_value(),self.y_bin.get_value())
        else:
            xmin=self.x_min.get_value()
            ymin=self.y_min.get_value()
            xparams=TBinAxisParams(xmin,xmin+self.x_max.get_value(),self.x_bin.get_value())
            yparams=TBinAxisParams(ymin,ymin+self.y_max.get_value(),self.y_bin.get_value())
        return self.validateROI(xparams,yparams)
    def _show_values(self, xparams, yparams):
        if self.kind=="minmax":
            xmax,ymax=xparams.max,yparams.max
        else:
            xmax,ymax=xparams.max-xparams.min,yparams.max-yparams.min
        self.x_min.set_value(xparams.min,notify_value_change=False)
        self.x_max.set_value(xmax,notify_value_change=False)
        self.x_bin.set_value(xparams.bin,notify_value_change=False)
        self.y_min.set_value(yparams.min,notify_value_change=False)
        self.y_max.set_value(ymax,notify_value_change=False)
        self.y_bin.set_value(yparams.bin,notify_value_change=False)
    def set_value(self, roi, notify_value_change=True):
        """
        Set ROI value.

        `roi` is a tuple ``(xparams, yparams)`` of two axes parameters (each is a 3-tuple ``(min, max, bin)``).
        If ``notify_value_change==True``, emit the `value_changed` signal; otherwise, change value silently.
        """
        roi=TBinAxisParams(*roi[0]),TBinAxisParams(*roi[1])
        params=self.validateROI(*roi)
        self._show_values(*params)
        if notify_value_change:
            self.value_changed.emit(params)