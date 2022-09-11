#pragma once

#include "../../NodeBase.h"
#include "../ParamServer_gen.h"

namespace BT_TEST
{
    namespace PARAM
    {
        class PARAM_b1 : public ParamBase<int>
        {
        public:
            PARAM_b1() : ParamBase<int>() {}
            virtual ~PARAM_b1() = default;

            int get() const override { return paramServer.get_b1(); }
            void set(const int &v) override { paramServer.set_b1(v); }
            Param getParamType() const override { return Param::b1__int; }
            char *getName() const override { return Cvt::getParamName(getParamType()); }

            delegate<int(void)> makeGetter() const override
            {
                delegate<int(void)> del;
                del.set<PARAM_b1, &PARAM_b1::get>(*this);
                return del;
            }

            delegate<void(const int &)> makeSetter() override
            {
                delegate<void(const int &)> del;
                del.set<PARAM_b1, &PARAM_b1::set>(*this);
                return del;
            }

        protected:
        };
    }
}