#pragma once

#include "../../NodeBase.h"
#include "../ParamServer_gen.h"

namespace BT_TEST
{
    namespace PARAM
    {
        template <bool IsBlackBoard>
        class PARAM_b3 : public ParamBase<float>
        {
        public:
            PARAM_b3() : ParamBase<float>() {}
            virtual ~PARAM_b3() = default;

            float get() override
            {
                if (IsBlackBoard)
                    return paramServer.get_b3();
                return this->_internal;
            }
            void set(const float &v) override
            {
                if (IsBlackBoard)
                    paramServer.set_b3(v);
                this->_internal = v;
            }
            Param getParamType() const override { return Param::b3__float; }

        protected:
        };
    }
}