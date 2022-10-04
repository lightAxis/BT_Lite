#pragma once

#include <stdint.h>
#include <assert.h>

#define @(NAMESPACE)_TOTAL_NODE_NUM (@(NODE_NUM))
#define @(NAMESPACE)_TOTAL_LOG_NUM (@(NAMESPACE)_TOTAL_NODE_NUM * 3)

namespace @(NAMESPACE)
{
    struct StatusChangeLog_t
    {
        union
        {
            struct
            {
                uint16_t uid : 12;
                uint8_t prev_status : 2;
                uint8_t status : 2;
            };
            uint16_t data;
        };
    };

    template <int TotalNodeNum>
    class Logger
    {
    public:
        Logger() {}
        ~Logger() = default;

        StatusChangeLog_t *getLogs()
        {
            return _logs;
        }

        void clearLogs()
        {
            for (uint16_t i = 0; i < TotalNodeNum * 3; i++)
            {
                _logs[i] = StatusChangeLog_t();
            }
            _log_idx = 0;
        }

        void addLog(const uint16_t &uid, const uint8_t &prev_status, const uint8_t &status)
        {
            StatusChangeLog_t new_log;
            new_log.uid = uid;
            new_log.prev_status = prev_status;
            new_log.status = status;
            _logs[_log_idx] = new_log;

            _log_idx++;

            printf("[logger] num:%d uid:%d, %s -> %s\n", _log_idx, uid, Cvt::getNodeStatusName((NodeStatus)prev_status), Cvt::getNodeStatusName((NodeStatus)status));

            assert(_log_idx < TotalNodeNum * 3); // logger index over
        }

        int getLogSize() { return _log_idx; }

    private:
        StatusChangeLog_t _logs[TotalNodeNum * 3];
        uint16_t _log_idx{0};
    };

    static Logger<@(NAMESPACE)_TOTAL_NODE_NUM> logger;
}