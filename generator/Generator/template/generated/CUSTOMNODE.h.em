@# em_globals
@# 
@# @dataclass
@# class Def_t:
@#     TypedefStr: str = None
@#     TypedefName: str = None
@#     VariableName: str = None
@#     
@# @dataclass
@# class TickFunc_t:
@#     before: List[str] = None
@#     Tick: str = None
@#     after: List[str] = None
@# 
@# NAMESPACE: str
@# DelegateInfos: List[Def_t]
@# TickDelInfo: Def_t
@# TickFuncInfo: TickFunc_t
@# ClassConstructorStr: str
@# ClassConstructorInits : List[str]
@# ClassName: str
@# NodeName: str
@# NodeType: str

#pragma once

#include "../../NodeBase.h"

namespace @(NAMESPACE)
{
    namespace NODE
    {
        class @(ClassName) : public @(NodeType)Base
        {
            // params delegate typedef
@[for del_info in DelegateInfos]@
            typedef @(del_info.TypedefStr) @(del_info.TypedefName);
@[end for]
        public:
            // delegate Typedef
            typedef @(TickDelInfo.TypedefStr) @(TickDelInfo.TypedefName);

            // constructor
            @(ClassName)(@(ClassConstructorStr)) : @(NodeType)Base(),
@{
print("\t\t\t\t"+", ".join(ClassConstructorInits)+"{}")
}@                                                                 
            virtual ~@(ClassName)() = default;

            @(NodeType) get@(NodeType)Type() const override { return @(NodeType)::@(NodeName); }
            char *getName() const override { return Cvt::get@(NodeType)Name(get@(NodeType)Type()); }

            NodeStatus TickContent() override
            {
                // prepare output values
@[for tempStr in TickFuncInfo.before]@
                @(tempStr);
@[end for]
                NodeStatus result = (*@(TickDelInfo.VariableName))(@(TickFuncInfo.Tick));
                // set output values
@[for tempStr in TickFuncInfo.after]@
                @(tempStr);
@[end for]
                return result;
            }

        private:
            // getter & setter
@[for del_info in DelegateInfos]
            @(del_info.TypedefName) @(del_info.VariableName);
@[end for]
            // tick delegate
            @(TickDelInfo.TypedefName) *@(TickDelInfo.VariableName);

        };
    }
}