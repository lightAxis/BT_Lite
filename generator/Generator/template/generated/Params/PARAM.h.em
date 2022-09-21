@# em globals
@# 
@# NAMESPACE: str
@# className: str
@# paramName: str
@# paramType: str 
@# 
#pragma once

#include "../../NodeBase.h"
#include "../ParamServer_gen.h"

namespace @(NAMESPACE)
{
    namespace PARAM
    {

        class @(className) : public ParamBase<@(paramType)>
        {
        public:
            @(className)() : ParamBase<@(paramType)>() {}
            virtual ~@(className)() = default;

            @(paramType) get() const override { return paramServer.get_@(paramName)(); }
            void set(const @(paramType)& v) override { paramServer.set_@(paramName)(v); }
            Param getParamType() const override { return Param::@(paramName); }
            char *getName() const override { return Cvt::getParamName(getParamType()); }

            delegate<@(paramType)(void)> makeGetter() const override
            {
                delegate<@(paramType)(void)> del;
                del.set<@(className), &@(className)::get>(*this);
                return del;
            }

            delegate<void(const @(paramType) &)> makeSetter() override
            {
                delegate<void(const @(paramType) &)> del;
                del.set<@(className), &@(className)::set>(*this);
                return del;
            }
        protected:
        };
    }
}