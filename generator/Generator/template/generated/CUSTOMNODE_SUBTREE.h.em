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
        public:
            // constructor
            @(ClassName)() : @(NodeType)Base(){}                                                         
            virtual ~@(ClassName)() = default;

            @(NodeType) get@(NodeType)Type() const override { return @(NodeType)::@(NodeName); }
            char *getName() const override { return Cvt::get@(NodeType)Name(get@(NodeType)Type()); }

            NodeStatus TickContent() override
            {
                NodeStatus result = this->_child->Tick();
                return result;
            }

        private:
        };
    }
}