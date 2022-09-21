#pragma once

#include "../../ParamBase.h"

namespace BT_TEST
{
    namespace PARAM
    {
        class PARAM_Const_int16_t : public ParamBase<int16_t>
        {
        public:
            PARAM_Const_int16_t() = delete;
            PARAM_Const_int16_t(const int16_t &v) : ParamBase<int16_t>(), _internal(v) {}
            virtual ~PARAM_Const_int16_t() = default;

            int16_t get() const override { return _internal; }
            void set(const int16_t &v) override { assert(0); } // PARAM_const cannot be set
            Param getParamType() const override { return Param::Const; }
            char *getName() const override { return Cvt::getParamName(getParamType()); }

            delegate<int16_t(void)> makeGetter() const override
            {
                delegate<int16_t(void)> del;
                del.set<PARAM_Const_int16_t, &PARAM_Const_int16_t::get>(*this);
                return del;
            }
            delegate<void(const int16_t &)> makeSetter() override
            {
                delegate<void(const int16_t &)> del;
                del.set<PARAM_Const_int16_t, &PARAM_Const_int16_t::set>(*this);
                return del;
            }

        private:
            const int16_t _internal;
        };
    }
}