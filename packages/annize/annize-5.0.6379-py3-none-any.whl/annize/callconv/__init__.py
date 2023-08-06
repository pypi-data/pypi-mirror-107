# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import dataclasses
import inspect
import typing as t

import annize.callconv.typehints


ParameterPredicate = t.Callable[[t.Any], bool]


def always_true(_: t.Any) -> bool:
    return True


@dataclasses.dataclass
class ParametersFromChildNodesInfos:
    parameter_name: str
    multiple: t.Optional[bool]
    if_passing: t.Optional[ParameterPredicate]
    if_typehint_matches: bool


def parameter_from_childnodes(paramname: str, multiple: t.Optional[bool] = None,
                              if_passing: t.Optional[ParameterPredicate] = None,
                              if_typehint_matches: bool = True):
    def decor(f):
        f._parametersfromchildnodes = getattr(f, "_parametersfromchildnodes", [])
        f._parametersfromchildnodes.append(ParametersFromChildNodesInfos(paramname, multiple, if_passing,
                                                                         if_typehint_matches))
        return f
    return decor


def get_parameters_from_childnodes_infos(calltype: t.Type) -> t.List[ParametersFromChildNodesInfos]:
    result = []
    for supertype in calltype.mro():
        supertypeconstructor = getattr(supertype, "__init__", supertype)
        result += getattr(supertypeconstructor, "_parametersfromchildnodes", None) or []
    calltypespec = inspect.getfullargspec(calltype)
    if not calltypespec.varkw:
        result = [info for info in result if info.parameter_name in calltypespec.kwonlyargs]
    return result


class _CallHelper:

    @staticmethod
    def __convert_kwargs_from_string(argumentinfos, args, kwargs):
        kwargs = dict(kwargs)
        for paramname, paramtypeinfo in argumentinfos.items():
            paramvalueorig = kwargs.get(paramname, None)
            if paramtypeinfo.is_constructable_from_string and isinstance(paramvalueorig, str):
                kwargs[paramname] = paramtypeinfo.construct_from_string(paramvalueorig)
        return args, kwargs

    @staticmethod
    def __shift_args_to_kwargs(calltype, argumentinfos, args, kwargs):
        for prminfo in annize.callconv.get_parameters_from_childnodes_infos(calltype):
            outerparamtypeinfo = argumentinfos.get(prminfo.parameter_name, None)
            if outerparamtypeinfo is None:
                raise TypeError(f"The '{prminfo.parameter_name}' argument specified in callconv on '{calltype}' does"
                                f" not exist")
            multiple = prminfo.multiple
            if_passing = prminfo.if_passing or always_true
            if multiple is None:
                multiple = isinstance(outerparamtypeinfo, annize.callconv.typehints.ListTypeInfo)
            if prminfo.if_typehint_matches:
                if multiple:
                    paramtypeinfo = outerparamtypeinfo.inner
                else:
                    paramtypeinfo = outerparamtypeinfo
                if_passing_orig = if_passing
                def if_passing(arg):  # pylint: disable=function-redefined
                    # pylint: disable=cell-var-from-loop
                    return if_passing_orig(arg) and paramtypeinfo.resolved_type \
                           and isinstance(arg, paramtypeinfo.resolved_type)
            argsnew = []
            kwargnew = []
            for arg in args:
                if if_passing(arg):
                    kwargnew.append(arg)
                else:
                    argsnew.append(arg)
            if multiple:
                kwargs[prminfo.parameter_name] = (kwargs.get(prminfo.parameter_name, None) or []) + kwargnew
            else:
                if len(kwargnew) > 1:
                    raise MultipleValuesForSingleArgumentError(prminfo.parameter_name)
                if len(kwargnew) == 1:
                    kwargs[prminfo.parameter_name] = kwargnew[0]
            args = argsnew
        return args, kwargs

    @classmethod
    def call(cls, calltype, args: t.Iterable, kwargs: t.Dict):
        argumentinfos = annize.callconv.typehints.get_arguments_infos(for_callable=calltype)
        args, kwargs = cls.__convert_kwargs_from_string(argumentinfos, args, kwargs)
        args, kwargs = cls.__shift_args_to_kwargs(calltype, argumentinfos, args, kwargs)
        return calltype(*args, **kwargs)


call = _CallHelper.call


class MultipleValuesForSingleArgumentError(TypeError):

    def __init__(self, argname: str):
        super().__init__(f"More than one value given for the single-value argument '{argname}'")
        self.argname = argname
