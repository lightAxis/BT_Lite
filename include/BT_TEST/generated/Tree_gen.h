#pragma once

#include "../Enums.h"
#include "../Params.h"
#include "../Nodes.h"

namespace BT_TEST
{
    class Tree
    {
    public:
        void set_CustomAction1_tickDel(NODE::ACTION_CustomAction1::_tickDel del) { _CustomAction1_tickDel = del; }
        void set_CustomAction2_tickDel(NODE::ACTION_CustomAction2::_tickDel del) { _CustomAction2_tickDel = del; }

        bool test()
        {
            if (_CustomAction1_tickDel == nullptr)
                return false;
            else if (_CustomAction2_tickDel == nullptr)
                return false;
            return true;
        }

        void build()
        {
            assert(test()); // all TickDelegate function pointers must not nullptr when build a tree

            _PARAM_b1__int.set(2);
            _PARAM_b2__int.set(3);
            _PARAM_b3__float.set(3.4f);
            _PARAM_b4__float.set(6.7);

            _SUBTREE_RootTree_1.addChild(&_CONTROL_Sequence_2);
            _CONTROL_Sequence_2.addChild(&_ACTION_AlwaysSuccess);
            _CONTROL_Sequence_2.addChild(&_CustomAction1_4);
            _CONTROL_Sequence_2.addChild(&_CustomAction2_5);
            _CONTROL_Sequence_2.addChild(&_CONTROL_Fallback_6);
            _CONTROL_Fallback_6.addChild(&_DECORATOR_Inverter_7);
            _CONTROL_Fallback_6.addChild(&_ACTION_AlwaysSuccess);
            _DECORATOR_Inverter_7.addChild(&_CustomAction1_9);
        }

        NodeStatus Tick()
        {
            return _SUBTREE_RootTree_1.Tick();
        }

    private:
        // Params Const
        PARAM::PARAM_Const_float _PARAM_Const_float_1{3};
        PARAM::PARAM_Const_float _PARAM_Const_float_2{53.4f};

        // Params Server
        PARAM::PARAM_b1 _PARAM_b1__int;
        PARAM::PARAM_b2 _PARAM_b2__int;
        PARAM::PARAM_b3 _PARAM_b3__float;
        PARAM::PARAM_b4 _PARAM_b4__float;

        // Nodes Tick Delegates
        NODE::ACTION_CustomAction1::_tickDel _CustomAction1_tickDel{nullptr};
        NODE::ACTION_CustomAction2::_tickDel _CustomAction2_tickDel{nullptr};

        // Nodes Tick Delegates Ptr
        NODE::ACTION_CustomAction1::_tickDel *_CustomAction1_tickDelPtr{&_CustomAction1_tickDel};
        NODE::ACTION_CustomAction2::_tickDel *_CustomAction2_tickDelPtr{&_CustomAction2_tickDel};

        // Nodes Singleton
        NODE::ACTION_AlwaysFailure _ACTION_AlwaysFailure{};
        NODE::ACTION_AlwaysSuccess _ACTION_AlwaysSuccess{};

        // Nodes Variable
        NODE::SUBTREE_RootTree _SUBTREE_RootTree_1{};
        NODE::CONTROL_Sequence<4> _CONTROL_Sequence_2{};
        // NODE::ACTION_AlwaysSuccess _ACTION_AlwaysSuccess_3{};
        NODE::ACTION_CustomAction1 _CustomAction1_4{_PARAM_Const_float_1.makeGetter(), _PARAM_b1__int.makeSetter(), _CustomAction1_tickDelPtr};
        NODE::ACTION_CustomAction2 _CustomAction2_5{_PARAM_b3__float.makeGetter(), _PARAM_b4__float.makeSetter(), _CustomAction2_tickDelPtr};
        NODE::CONTROL_Fallback<2> _CONTROL_Fallback_6{};
        NODE::DECORATOR_Inverter _DECORATOR_Inverter_7{};
        // NODE::ACTION_AlwaysSuccess _ACTION_AlwaySuccess_8{};
        NODE::ACTION_CustomAction1 _CustomAction1_9{_PARAM_b4__float.makeGetter(), _PARAM_b2__int.makeSetter(), _CustomAction1_tickDelPtr};
    };
}