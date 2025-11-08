//+------------------------------------------------------------------+
//|                                                        MTF_MA_AI.mq5 |
//|                                              Copyright 2025, AI Trade |
//|                                             https://www.yoursite.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2025, AI Trade"
#property link      "https://www.yoursite.com"
#property version   "1.00"

// Import necessary libraries
#include <Trade\Trade.mqh>
#include <Python\Python.mqh>

// Global variables
CTrade trade;
int handle;
string python_path = "d:\\New folder\\Trd\\mt5_ai_trading\\venv\\Scripts\\python.exe";
string script_path = "d:\\New folder\\Trd\\mt5_ai_trading\\mt5_interface.py";

//+------------------------------------------------------------------+
//| Expert initialization function                                     |
//+------------------------------------------------------------------+
int OnInit()
{
    // Initialize Python
    if(!PythonInitialize(python_path))
    {
        Print("Error initializing Python: ", GetLastError());
        return INIT_FAILED;
    }
    
    // Train the model with historical data
    if(!TrainModel())
    {
        Print("Error training model");
        return INIT_FAILED;
    }
    
    return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                   |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    PythonDeinitialize();
}

//+------------------------------------------------------------------+
//| Expert tick function                                              |
//+------------------------------------------------------------------+
void OnTick()
{
    // Get prediction from AI model
    string signal = GetPrediction();
    if(signal == "") return;
    
    // Process trading signal
    ProcessSignal(signal);
}

//+------------------------------------------------------------------+
//| Train the AI model with historical data                           |
//+------------------------------------------------------------------+
bool TrainModel()
{
    // Get historical data
    MqlRates rates[];
    ArraySetAsSeries(rates, true);
    int copied = CopyRates(_Symbol, PERIOD_M15, 0, 2000, rates);
    
    if(copied <= 0)
    {
        Print("Error copying historical data: ", GetLastError());
        return false;
    }
    
    // Convert data to JSON
    string json = RatesToJSON(rates);
    
    // Call Python function to train model
    string result = PythonExecuteString("from mt5_interface import MT5Interface; \
                                       interface = MT5Interface(); \
                                       print(interface.train_model('" + json + "'))");
                                       
    if(StringFind(result, "Error") >= 0)
    {
        Print("Training error: ", result);
        return false;
    }
    
    return true;
}

//+------------------------------------------------------------------+
//| Get prediction from AI model                                      |
//+------------------------------------------------------------------+
string GetPrediction()
{
    // Get latest data
    MqlRates rates[];
    ArraySetAsSeries(rates, true);
    int copied = CopyRates(_Symbol, PERIOD_M15, 0, 100, rates);
    
    if(copied <= 0)
    {
        Print("Error copying latest data: ", GetLastError());
        return "";
    }
    
    // Convert data to JSON
    string json = RatesToJSON(rates);
    
    // Get prediction from Python
    string result = PythonExecuteString("from mt5_interface import MT5Interface; \
                                       interface = MT5Interface(); \
                                       print(interface.get_prediction('" + json + "'))");
                                       
    return result;
}

//+------------------------------------------------------------------+
//| Convert MqlRates array to JSON string                             |
//+------------------------------------------------------------------+
string RatesToJSON(MqlRates &rates[])
{
    string json = "[";
    for(int i = 0; i < ArraySize(rates); i++)
    {
        if(i > 0) json += ",";
        json += "{";
        json += "\"time\":" + (string)rates[i].time + ",";
        json += "\"open\":" + DoubleToString(rates[i].open, _Digits) + ",";
        json += "\"high\":" + DoubleToString(rates[i].high, _Digits) + ",";
        json += "\"low\":" + DoubleToString(rates[i].low, _Digits) + ",";
        json += "\"close\":" + DoubleToString(rates[i].close, _Digits) + ",";
        json += "\"volume\":" + (string)rates[i].tick_volume;
        json += "}";
    }
    json += "]";
    return json;
}

//+------------------------------------------------------------------+
//| Process trading signal from AI                                    |
//+------------------------------------------------------------------+
void ProcessSignal(string signal)
{
    // Parse JSON response
    if(StringFind(signal, "error") >= 0)
    {
        Print("Error in prediction: ", signal);
        return;
    }
    
    // Extract signal from JSON
    string trade_signal = "";
    if(StringFind(signal, "BUY") >= 0)
        trade_signal = "BUY";
    else if(StringFind(signal, "SELL") >= 0)
        trade_signal = "SELL";
    else
        return; // Neutral signal
        
    // Check if we already have a position
    if(PositionsTotal() > 0)
        return;
        
    // Place trade
    double volume = 0.1;  // Default lot size
    double sl = 0, tp = 0;
    
    if(trade_signal == "BUY")
    {
        sl = SymbolInfoDouble(_Symbol, SYMBOL_BID) - (50 * _Point);
        tp = SymbolInfoDouble(_Symbol, SYMBOL_ASK) + (100 * _Point);
        trade.Buy(volume, _Symbol, 0, sl, tp, "AI Trade");
    }
    else if(trade_signal == "SELL")
    {
        sl = SymbolInfoDouble(_Symbol, SYMBOL_ASK) + (50 * _Point);
        tp = SymbolInfoDouble(_Symbol, SYMBOL_BID) - (100 * _Point);
        trade.Sell(volume, _Symbol, 0, sl, tp, "AI Trade");
    }
}