#include <iostream>

// Product interface
class Document {
public:
    virtual void open() = 0;
    virtual void save() = 0;
    virtual ~Document() = default;
};

// Concrete products
class TextDocument : public Document {
public:
    void open() override { std::cout << "Opening text document\n"; }
    void save() override { std::cout << "Saving text document\n"; }
};

class SpreadsheetDocument : public Document {
public:
    void open() override { std::cout << "Opening spreadsheet\n"; }
    void save() override { std::cout << "Saving spreadsheet\n"; }
};

// Creator
class Application {
public:
    virtual Document* createDocument() = 0;
    
    void newDocument() {
        Document* doc = createDocument();
        doc->open();
        // Store document...
    }
};

// Concrete creators
class TextApplication : public Application {
public:
    Document* createDocument() override {
        return new TextDocument();
    }
};

class SpreadsheetApplication : public Application {
public:
    Document* createDocument() override {
        return new SpreadsheetDocument();
    }
};