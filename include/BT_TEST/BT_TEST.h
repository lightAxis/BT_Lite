#pragma once

#include "Enums.h"
#include "Nodes.h"
#include "Params.h"

namespace BT_TEST
{

    static void
    test()
    {
        NODE::CONTROL_IfThenElse<3> ifthenelse;

        NODE::ACTION_AlwaysSuccess succ1;
        NODE::ACTION_AlwaysFailure fail1;

        PARAM::PARAM_Const_uint8_t uint8t(5);
        PARAM::PARAM_Const_uint8_t uint8t2(3);

        NODE::CONTROL_Parallel<6> para{uint8t.makeGetter(), uint8t2.makeGetter()};
        para.addChild(&succ1);
        para.addChild(&succ1);
        para.addChild(&fail1);
        para.addChild(&succ1);
        para.addChild(&fail1);
        para.addChild(&succ1);

        para.Tick();

        return;
    }
}
