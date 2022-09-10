#pragma once

#include "Enums.h"
#include "Delegate.h"

#include <stddef.h>
#include <stdint.h>

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
            NodeBase() : _uid(makeUID()), _status(NodeStatus::IDLE) {}
            virtual ~NodeBase() = default;

            uint16_t getUID() { return _uid; }
            NodeStatus getStatus() { return _status; }
            void setStatus(NodeStatus status) { _status = status; }

            virtual NodeType getType() const = 0;
            virtual char *getName() const = 0;

            virtual NodeStatus Tick() = 0;
            virtual void Reset() = 0;

        protected:
            NodeStatus _status;
            const uint16_t _uid;
        };

        class ActionBase : public NodeBase
        {
        public:
            ActionBase() : NodeBase() {}
            virtual ~ActionBase() = default;
            NodeType getType() const override { return NodeType::ACTION; }

            virtual Action getActionType() const = 0;

        protected:
        };

        class ConditionBase : public NodeBase
        {
        public:
            ConditionBase() : NodeBase() {}
            virtual ~ConditionBase() = default;
            NodeType getType() const override { return NodeType::CONDITION; }

            virtual Condition getConditionType() const = 0;

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
                if (_child_num >= ChildN)
                    return false;

                _children[_child_num] = child;
                return true;
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

            bool setChild(NodeBase *child)
            {
                if (_child != nullptr)
                    return false;

                _child = child;
                return true;
            }

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

            bool setChild(NodeBase *child)
            {
                if (_child != nullptr)
                    return false;

                _child = child;
                return true;
            }

        protected:
            NodeBase *_child;
        };
    }

    namespace PARAM
    {
        template <typename T>
        class ParamBase
        {
        public:
            ParamBase(){};
            virtual ~ParamBase() = default;

            virtual T get() = 0;
            virtual void set(const T &v) = 0;
            virtual Param getParamType() const = 0;

        protected:
            T _internal;
        };
    }

}