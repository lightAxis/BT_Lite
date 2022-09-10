#pragma once

#include "../../NodeBase.h"
#include "../ParamServer_gen.h"

namespace BT_TEST
{
    namespace PARAM
    {

        class PARAM_b4 : public ParamBase<float>
        {
        public:
            PARAM_b4() : ParamBase<float>() {}
            virtual ~PARAM_b4() = default;

            float get() const override { return paramServer.get_b4(); }
            void set(const float &v) override { paramServer.set_b4(v); }
            Param getParamType() const override { return Param::b4__float; }

        protected:
        };
    }
}