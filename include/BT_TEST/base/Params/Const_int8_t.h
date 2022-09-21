#pragma once

#include "../../ParamBase.h"

namespace BT_TEST
{
    namespace PARAM
    {
        class PARAM_Const_int8_t : public ParamBase<int8_t>
        {
        public:
            PARAM_Const_int8_t() = delete;
            PARAM_Const_int8_t(const int8_t &v) : ParamBase<int8_t>(), _internal(v) {}
            virtual ~PARAM_Const_int8_t() = default;

            int8_t get() const override { return _internal; }
            void set(const int8_t &v) override { assert(0); } // PARAM_const cannot be set
            Param getParamType() const override { return Param::Const; }
            char *getName() const override { return Cvt::getParamName(getParamType()); }

            delegate<int8_t(void)> makeGetter() const override
            {
                delegate<int8_t(void)> del;
                del.set<PARAM_Const_int8_t, &PARAM_Const_int8_t::get>(*this);
                return del;
            }
            delegate<void(const int8_t &)> makeSetter() override
            {
                delegate<void(const int8_t &)> del;
                del.set<PARAM_Const_int8_t, &PARAM_Const_int8_t::set>(*this);
                return del;
            }

        private:
            const int8_t _internal;
        };
    }
}