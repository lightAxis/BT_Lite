#pragma once

#include "../../NodeBase.h"

namespace BT_TEST
{
    namespace PARAM
    {
        class PARAM_Const_uint8_t : public ParamBase<uint8_t>
        {
        public:
            PARAM_Const_uint8_t() = delete;
            PARAM_Const_uint8_t(const uint8_t &v) : ParamBase<uint8_t>(), _internal(v) {}
            virtual ~PARAM_Const_uint8_t() = default;

            uint8_t get() const override { return _internal; }
            void set(const uint8_t &v) override { assert(0); } // PARAM_const cannot be set
            Param getParamType() const override { return Param::Const; }
            char *getName() const override { return Cvt::getParamName(getParamType()); }

            delegate<uint8_t(void)> makeGetter() const override
            {
                delegate<uint8_t(void)> del;
                del.set<PARAM_Const_uint8_t, &PARAM_Const_uint8_t::get>(*this);
                return del;
            }
            delegate<void(const uint8_t &)> makeSetter() override
            {
                delegate<void(const uint8_t &)> del;
                del.set<PARAM_Const_uint8_t, &PARAM_Const_uint8_t::set>(*this);
                return del;
            }

        private:
            const uint8_t _internal;
        };
    }
}