#pragma once

#include "../../NodeBase.h"
#include "../ParamServer_gen.h"

namespace BT_TEST
{
    namespace PARAM
    {
        template <bool IsBlackBoard>
        class PARAM_b1 : public ParamBase<int>
        {
        public:
            PARAM_b1() : ParamBase<int>() {}
            virtual ~PARAM_b1() = default;

            int get() override
            {
                if (IsBlackBoard)
                    return paramServer.get_b1();
                return this->_internal;
            }
            void set(const int &v) override
            {
                if (IsBlackBoard)
                    paramServer.set_b1(v);
                this->_internal = v;
            }
            Param getParamType() const override { return Param::b1__int; }

        protected:
        };
    }
}