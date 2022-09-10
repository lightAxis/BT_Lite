#pragma once

#include "../../NodeBase.h"
#include "../ParamServer_gen.h"

namespace BT_TEST
{
    namespace PARAM
    {
        class PARAM_b3 : public ParamBase<float>
        {
        public:
            PARAM_b3() : ParamBase<float>() {}
            virtual ~PARAM_b3() = default;

            float get() const override { return paramServer.get_b3(); }
            void set(const float &v) override { paramServer.set_b3(v); }
            Param getParamType() const override { return Param::b3__float; }

        protected:
        };
    }
}