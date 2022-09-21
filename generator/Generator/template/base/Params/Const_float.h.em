#pragma once

#include "../../NodeBase.h"

namespace @(NAMESPACE)
{
    namespace PARAM
    {
        class PARAM_Const_float : public ParamBase<float>
        {
        public:
            PARAM_Const_float() = delete;
            PARAM_Const_float(const float &v) : ParamBase<float>(), _internal(v)
            {
                float aa = _internal;
                _a = aa;
            }
            virtual ~PARAM_Const_float() = default;

            float get() const override
            {
                return _a;
            }
            void set(const float &v) override { assert(0); } // PARAM_const cannot be set
            Param getParamType() const override { return Param::Const; }
            char *getName() const override { return Cvt::getParamName(getParamType()); }

            delegate<float(void)> makeGetter() const override
            {
                delegate<float(void)> del;
                del.set<PARAM_Const_float, &PARAM_Const_float::get>(*this);
                return del;
            }
            delegate<void(const float &)> makeSetter() override
            {
                delegate<void(const float &)> del;
                del.set<PARAM_Const_float, &PARAM_Const_float::set>(*this);
                return del;
            }

        private:
            const float _internal;
            float _a;
        };
    }
}