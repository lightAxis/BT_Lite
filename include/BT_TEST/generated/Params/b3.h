#pragma once

#include "../../ParamBase.h"
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
            char *getName() const override { return Cvt::getParamName(getParamType()); }

            delegate<float(void)> makeGetter() const override
            {
                delegate<float(void)> del;
                del.set<PARAM_b3, &PARAM_b3::get>(*this);
                return del;
            }

            delegate<void(const float &)> makeSetter() override
            {
                delegate<void(const float &)> del;
                del.set<PARAM_b3, &PARAM_b3::set>(*this);
                return del;
            }

        protected:
        };
    }
}