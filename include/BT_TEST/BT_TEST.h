#pragma once

#include "Enums.h"
#include "Nodes.h"
#include "Params.h"

namespace BT_TEST
{

    namespace NODE
    {
        class AlwaysRunning : public ActionBase
        {
        public:
            AlwaysRunning() : ActionBase() {}
            virtual ~AlwaysRunning() = default;

            Action getActionType() const override { return Action::CustomAction1; }
            char *getName() const override { return Cvt::getActionName(getActionType()); }
            NodeStatus Tick() override
            {
                printf("name:%s, uid:%d Ticked\n", getName(), this->getUID());
                return getStatus();
            }
            void Reset() override {}

        private:
        };
    }

    static void
    test()
    {
        NODE::CONTROL_IfThenElse<3> ifthenelse;

        NODE::ACTION_AlwaysSuccess succ1;
        NODE::ACTION_AlwaysFailure fail1;
        NODE::AlwaysRunning runn1;
        runn1.setStatus(NodeStatus::RUNNING);

        PARAM::PARAM_Const_uint8_t u1(5);
        PARAM::PARAM_Const_uint8_t u2(3);
        PARAM::PARAM_Const_uint8_t u3(32);

        NODE::CONTROL_WhileDoElse<3> wde;

        wde.addChild(&succ1);
        wde.addChild(&runn1);
        wde.addChild(&fail1);

        // wde.Tick();
        // wde.Tick();

        NODE::CONTROL_IfThenElse<3> ite;
        ite.addChild(&succ1);
        ite.addChild(&runn1);
        ite.addChild(&fail1);

        ite.Tick();
        ite.Tick();
        runn1.setStatus(NodeStatus::FAILURE);
        ite.Tick();
        ite.Tick();
        ite.Tick();

        return;
    }
}
