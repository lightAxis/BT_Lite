@# em_globals
@# 'NAMESPACE': str
@# @dataclass
@# class NodeNames_t:
@#     className: str = None
@#     variableName: str = None
@#     initializeStr: str = None
@# 
@# @dataclass
@# class DelegateNames_t:
@#     className: str = None
@#     variableName: str = None
@#     initializeStr: str = None
@#     classNamePtr: str = None
@#     variableNamePtr: str = None
@#     initializeStrPtr: str = None
@# 
@# @dataclass
@# class ParamNames_t:
@#     className: str = None
@#     variableName: str = None
@#     initializeStr: str = None
@# 
@# NodeName_List: List[NodeNames_t] = []
@# DelegateName_List: List[DelegateNames_t] = []
@# ConstParamName_List: List[ParamNames_t] = []
@# CustomParamName_List: List[ParamNames_t] = []
@# BuildStr_List: List[str] = []
@# 
#pragma once

#include "../Enums.h"
#include "../Params.h"
#include "../Nodes.h"

namespace @(NAMESPACE)
{
    class Tree
    {
    public:
@[for del_t in DelegateName_List]@
        void set@(del_t.variableName)(NODE::@(del_t.className) del) {@(del_t.variableName) = del; }
@[end for]
        bool test()
        {
@{
delLen = len(DelegateName_List)
delIdx = 1
if delLen >0:
    tabs = "\t\t\t"
    print(tabs, "if(")
    for del_t in DelegateName_List:
        backward:str = ""
        if delIdx == delLen:
            backward = ")"
        else:
            backward = "||"
        print(tabs, del_t.variableName," == ", del_t.initializeStr, backward)
        delIdx = delIdx + 1
    print(tabs, "\t", "return false;")
}@
            return true;
        }

        void build()
        {
            assert(test()); // all TickDelegate function pointers must not nullptr when build a tree

            //_PARAM_b1__int.set(2);
            //_PARAM_b2__int.set(3);
            //_PARAM_b3__float.set(3.4f);
            //_PARAM_b4__float.set(6.7);
@[for Str in BuildStr_List]@
            @(Str)
@[end for]
        }

        NodeStatus Tick()
        {
            return @(NodeName_List[0].variableName).Tick();
        }

    private:
        // Params Const
@[for param in ConstParamName_List]@
        PARAM::@(param.className) @(param.variableName){@param.initializeStr};
@[end for]
        // Params Server
@[for param in CustomParamName_List]@
        PARAM::@(param.className) @(param.variableName){@param.initializeStr};
@[end for]
        // Nodes Tick Delegates
@[for del_t in DelegateName_List]@
        NODE::@(del_t.className) @(del_t.variableName){@(del_t.initializeStr)};
@[end for]
        // Nodes Tick Delegates Ptr
@[for del_t in DelegateName_List]@
        NODE::@(del_t.classNamePtr) @(del_t.variableNamePtr){@(del_t.initializeStrPtr)};
@[end for]    
        // Nodes Variable
@[for node_t in NodeName_List]@
        NODE::@(node_t.className) @(node_t.variableName){@(node_t.initializeStr)};
@[end for]
    };
}