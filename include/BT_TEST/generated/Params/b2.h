#pragma once

#include "../../NodeBase.h"
#include "../ParamServer_gen.h"

namespace BT_TEST
{
    namespace PARAM
    {
        template <bool IsBlackBoard>
        class PARAM_b2 : public ParamBase<int>
        {
        public:
            PARAM_b2() : ParamBase<int>() {}
            virtual ~PARAM_b2() = default;

            int get() override
            {
                if (IsBlackBoard)
                    return paramServer.get_b2();
                return this->_internal;
            }
            void set(const int &v) override
            {
                if (IsBlackBoard)
                    paramServer.set_b2(v);
                this->_internal = v;
            }
            Param getParamType() const override { return Param::b2__int; }

        protected:
        };
    }
}