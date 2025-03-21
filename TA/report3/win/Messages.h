#ifndef MESSAGES_H
#define MESSAGES_H

#include <string>
#include <vector>

class Messages {
private:
    std::vector<std::string> messages;

public:
    Messages();
    Messages(const std::string& message_string);
    Messages(const std::vector<std::string>& message_vector);
    ~Messages();

    void addMessage(const std::string& message_string);
    std::string getMessage(int message_id);
    void showAllMessages();
    int getNMessages();
};

#endif // MESSAGES_H
