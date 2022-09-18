#pragma once

#include "../../NodeBase.h"

namespace @(NAMESPACE)
{
    namespace PARAM
    {
        class PARAM_Const_bool : public ParamBase<bool>
        {
        public:
            PARAM_Const_bool() = delete;
            PARAM_Const_bool(const bool &v) : ParamBase<bool>(), _internal(v) {}
            virtual ~PARAM_Const_bool() = default;

            bool get() const override { return _internal; }
            void set(const bool &v) override { assert(0); } // PARAM_const cannot be set
            Param getParamType() const override { return Param::Const; }
            char *getName() const override { return Cvt::getParamName(getParamType()); }

            delegate<bool(void)> makeGetter() const override
            {
                delegate<bool(void)> del;
                del.set<PARAM_Const_bool, &PARAM_Const_bool::get>(*this);
                return del;
            }
            delegate<void(const bool &)> makeSetter() override
            {
                delegate<void(const bool &)> del;
                del.set<PARAM_Const_bool, &PARAM_Const_bool::set>(*this);
                return del;
            }

        private:
            const bool _internal;
        };
    }
}