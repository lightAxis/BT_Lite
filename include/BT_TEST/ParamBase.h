#pragma once

#include "Enums.h"
#include "Delegate.h"

#include <stddef.h>
#include <stdint.h>
#include <assert.h>

namespace BT_TEST
{
    namespace PARAM
    {
        template <typename T>
        class ParamBase
        {
        public:
            ParamBase(){};
            virtual ~ParamBase() = default;

            virtual T get() const = 0;
            virtual void set(const T &v) = 0;
            virtual Param getParamType() const = 0;
            virtual char *getName() const = 0;

            virtual delegate<T(void)> makeGetter() const = 0;
            virtual delegate<void(const T &)> makeSetter() = 0;

        protected:
        };
    }
}