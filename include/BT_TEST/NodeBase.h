#pragma once

#include "Enums.h"
#include "Delegate.h"
#include "Logger.h"

#include <stddef.h>
#include <stdint.h>
#include <assert.h>

namespace BT_TEST
{
    namespace NODE
    {
        static uint16_t makeUID()
        {
            static uint16_t uid = 1;
            return uid++;
        }

        class NodeBase
        {
        public:
            NodeBase() : _status(NodeStatus::IDLE), _uid(makeUID()) {}
            virtual ~NodeBase() = default;

            uint16_t getUID() { return _uid; }
            NodeStatus getStatus() { return _status; }
            void setStatus(NodeStatus status)
            {
                logger.addLog(_uid, (uint8_t)(_status), (uint8_t)(status));
                _status = status;
            }

            virtual NodeType getType() const = 0;
            virtual char *getName() const = 0;

            void Reset() { setStatus(NodeStatus::IDLE); }
            virtual void ResetChildren() = 0;
            virtual NodeStatus TickContent() = 0;

            NodeStatus Tick()
            {
                // printf("[NodeBase]-----");
                // printf("name:%s, uid:%d Ticked\n", getName(), getUID());
                setStatus(NodeStatus::RUNNING);
                NodeStatus result = TickContent();
                ResetChildren();
                setStatus(result);
                // printf("[NodeBase]-----");
                // printf("name:%s, uid:%d finished:%s\n", getName(), getUID(), Cvt::getNodeStatusName(getStatus()));
                return result;
            }

        private:
            NodeStatus _status;
            uint16_t _uid{0};
        };

        class ActionBase : public NodeBase
        {
        public:
            ActionBase() : NodeBase() {}
            virtual ~ActionBase() = default;
            NodeType getType() const override { return NodeType::ACTION; }

            virtual Action getActionType() const = 0;
            void ResetChildren() override {}

        protected:
        };

        class ConditionBase : public NodeBase
        {
        public:
            ConditionBase() : NodeBase() {}
            virtual ~ConditionBase() = default;
            NodeType getType() const override { return NodeType::CONDITION; }

            virtual Condition getConditionType() const = 0;
            void ResetChildren() override {}

        protected:
        };

        template <uint8_t ChildN>
        class ControlBase : public NodeBase
        {
        public:
            ControlBase() : NodeBase(), _child_num(0)
            {
                for (uint8_t i = 0; i < ChildN; i++)
                {
                    _children[i] = nullptr;
                }
            }
            virtual ~ControlBase() = default;
            NodeType getType() const override { return NodeType::CONTROL; }

            virtual Control getControlType() const = 0;

            bool addChild(NodeBase *child)
            {
                assert(_child_num < ChildN);

                if (_child_num >= ChildN)
                    return false;

                _children[_child_num] = child;
                _child_num++;
                return true;
            }

            void ResetChildren() override
            {
                for (uint8_t i = 0; i < _child_num; i++)
                    _children[i]->Reset();
            }

        protected:
            NodeBase *_children[ChildN];
            uint8_t _child_num;
        };

        class DecoratorBase : public NodeBase
        {
        public:
            DecoratorBase() : NodeBase(), _child{nullptr} {}
            virtual ~DecoratorBase() = default;
            NodeType getType() const override { return NodeType::DECORATOR; }

            virtual Decorator getDecoratorType() const = 0;

            bool addChild(NodeBase *child)
            {
                assert(_child == nullptr);

                if (_child != nullptr)
                    return false;

                _child = child;
                return true;
            }

            void ResetChildren() override { _child->Reset(); }

        protected:
            NodeBase *_child;
        };

        class SubTreeBase : public NodeBase
        {
        public:
            SubTreeBase() : NodeBase() {}
            virtual ~SubTreeBase() = default;
            NodeType getType() const override { return NodeType::SUBTREE; }

            virtual SubTree getSubTreeType() const = 0;

            bool addChild(NodeBase *child)
            {
                assert(_child == nullptr);

                if (_child != nullptr)
                    return false;

                _child = child;
                return true;
            }

            void ResetChildren() override { _child->Reset(); }

        protected:
            NodeBase *_child;
        };
    }
}
