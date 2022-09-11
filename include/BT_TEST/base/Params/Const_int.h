#pragma once

#include "../../NodeBase.h"

namespace BT_TEST
{
    namespace PARAM
    {
        class PARAM_Const_int : public ParamBase<int>
        {
        public:
            PARAM_Const_int() = delete;
            PARAM_Const_int(const int &v) : ParamBase<int>(), _internal(v) {}
            virtual ~PARAM_Const_int() = default;

            int get() const override { return _internal; }
            void set(const int &v) override { assert(0); } // PARAM_const cannot be set
            Param getParamType() const override { return Param::Const; }
            char *getName() const override { return Cvt::getParamName(getParamType()); }

            delegate<int(void)> makeGetter() const override
            {
                delegate<int(void)> del;
                del.set<PARAM_Const_int, &PARAM_Const_int::get>(*this);
                return del;
            }
            delegate<void(const int &)> makeSetter() override
            {
                delegate<void(const int &)> del;
                del.set<PARAM_Const_int, &PARAM_Const_int::set>(*this);
                return del;
            }

        private:
            const int _internal;
        };
    }
}