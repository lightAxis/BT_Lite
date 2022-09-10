#pragma once

#include "../../NodeBase.h"
#include "../ParamServer_gen.h"

namespace BT_TEST
{
    namespace PARAM
    {
        class PARAM_b2 : public ParamBase<int>
        {
        public:
            PARAM_b2() : ParamBase<int>() {}
            virtual ~PARAM_b2() = default;

            int get() const override { return paramServer.get_b2(); }
            void set(const int &v) override { paramServer.set_b2(v); }
            Param getParamType() const override { return Param::b2__int; }

        protected:
        };
    }
}