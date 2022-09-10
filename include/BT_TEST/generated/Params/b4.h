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

            delegate<float(void)> makeGetter() const override
            {
                delegate<float(void)> del;
                del.set<PARAM_b4, &PARAM_b4::get>(*this);
                return del;
            }

            delegate<void(const float &)> makeSetter() override
            {
                delegate<void(const float &)> del;
                del.set<PARAM_b4, &PARAM_b4::set>(*this);
                return del;
            }

        protected:
        };
    }
}