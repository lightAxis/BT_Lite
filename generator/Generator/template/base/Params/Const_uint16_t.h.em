#pragma once

#include "../../ParamBase.h"

namespace @(NAMESPACE)
{
    namespace PARAM
    {
        class PARAM_Const_uint16_t : public ParamBase<uint16_t>
        {
        public:
            PARAM_Const_uint16_t() = delete;
            PARAM_Const_uint16_t(const uint16_t &v) : ParamBase<uint16_t>(), _internal(v) {}
            virtual ~PARAM_Const_uint16_t() = default;

            uint16_t get() const override { return _internal; }
            void set(const uint16_t &v) override { assert(0); } // PARAM_const cannot be set
            Param getParamType() const override { return Param::Const; }
            char *getName() const override { return Cvt::getParamName(getParamType()); }

            delegate<uint16_t(void)> makeGetter() const override
            {
                delegate<uint16_t(void)> del;
                del.set<PARAM_Const_uint16_t, &PARAM_Const_uint16_t::get>(*this);
                return del;
            }
            delegate<void(const uint16_t &)> makeSetter() override
            {
                delegate<void(const uint16_t &)> del;
                del.set<PARAM_Const_uint16_t, &PARAM_Const_uint16_t::set>(*this);
                return del;
            }

        private:
            const uint16_t _internal;
        };
    }
}