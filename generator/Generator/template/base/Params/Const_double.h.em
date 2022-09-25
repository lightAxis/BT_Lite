#pragma once

#include "../../ParamBase.h"

namespace @(NAMESPACE)
{
    namespace PARAM
    {
        class PARAM_Const_double : public ParamBase<double>
        {
        public:
            PARAM_Const_double() = delete;
            PARAM_Const_double(const double &v) : ParamBase<double>(), _internal(v) {}
            virtual ~PARAM_Const_double() = default;

            double get() const override { return _internal; }
            void set(const double &v) override { assert(0); } // PARAM_const cannot be set
            Param getParamType() const override { return Param::Const; }
            char *getName() const override { return Cvt::getParamName(getParamType()); }

            delegate<double(void)> makeGetter() const override
            {
                delegate<double(void)> del;
                del.set<PARAM_Const_double, &PARAM_Const_double::get>(*this);
                return del;
            }
            delegate<void(const double &)> makeSetter() override
            {
                delegate<void(const double &)> del;
                del.set<PARAM_Const_double, &PARAM_Const_double::set>(*this);
                return del;
            }

        private:
            const double _internal;
        };
    }
}