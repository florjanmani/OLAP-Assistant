import { useState, useEffect, useRef, useCallback } from "react";
import axios from "axios";
import { toast } from "sonner";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Send,
  Database,
  TrendingUp,
  BarChart3,
  ArrowDown,
  ArrowUp,
  Filter,
  RotateCcw,
  Layers,
  MessageSquare,
  Sparkles,
  Moon,
  Sun,
} from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
} from "recharts";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const CHART_COLORS = ["#0047AB", "#FF3B30", "#00C7BE", "#AF52DE", "#FF9500"];

// Chat Message Component
const ChatMessage = ({ message }) => {
  const isUser = message.role === "user";

  return (
    <div
      className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4 animate-slide-up`}
      data-testid={`chat-message-${message.role}`}
    >
      <div
        className={`max-w-[80%] ${
          isUser ? "chat-message-user" : "chat-message-assistant"
        } px-4 py-3`}
      >
        <p className="text-sm whitespace-pre-wrap">{message.content}</p>
        {message.analysis_result && (
          <div className="mt-2 pt-2 border-t border-current/20">
            <Badge variant="outline" className="text-xs">
              {message.analysis_result.row_count} results found
            </Badge>
          </div>
        )}
      </div>
    </div>
  );
};

// Results Table Component
const ResultsTable = ({ data, dimensions }) => {
  if (!data || data.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">
        <Database className="w-12 h-12 mx-auto mb-3 opacity-50" />
        <p>No results to display</p>
      </div>
    );
  }

  const columns = Object.keys(data[0]);

  return (
    <div className="overflow-x-auto">
      <Table className="data-table">
        <TableHeader>
          <TableRow>
            {columns.map((col) => (
              <TableHead key={col} className="font-semibold">
                {col.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase())}
              </TableHead>
            ))}
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((row, idx) => (
            <TableRow key={idx}>
              {columns.map((col) => (
                <TableCell key={col} className="font-mono">
                  {typeof row[col] === "number"
                    ? row[col].toLocaleString("en-US", {
                        maximumFractionDigits: 2,
                      })
                    : row[col]}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};

// Results Chart Component
const ResultsChart = ({ data, dimensions }) => {
  if (!data || data.length === 0) return null;

  const chartData = data.slice(0, 10).map((item) => ({
    name: dimensions.map((d) => item[d]).join(" - "),
    value: item.total_sales_amount || 0,
    quantity: item.total_quantity || 0,
  }));

  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
          <XAxis
            dataKey="name"
            tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }}
            angle={-45}
            textAnchor="end"
            height={80}
          />
          <YAxis
            tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }}
            tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`}
          />
          <Tooltip
            contentStyle={{
              background: "hsl(var(--card))",
              border: "1px solid hsl(var(--border))",
              borderRadius: "4px",
            }}
            formatter={(value) => [`$${value.toLocaleString()}`, "Sales"]}
          />
          <Bar dataKey="value" fill={CHART_COLORS[0]} radius={[2, 2, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

// Metric Card Component
const MetricCard = ({ label, value, icon: Icon, trend }) => (
  <Card className="metric-card border-border">
    <CardContent className="p-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="metric-label">{label}</p>
          <p className="metric-value mt-1">{value}</p>
        </div>
        <div className="p-3 bg-primary/10 rounded-sm">
          <Icon className="w-5 h-5 text-primary" />
        </div>
      </div>
      {trend && (
        <div className="mt-2 flex items-center text-xs text-muted-foreground">
          {trend > 0 ? (
            <ArrowUp className="w-3 h-3 text-green-500 mr-1" />
          ) : (
            <ArrowDown className="w-3 h-3 text-red-500 mr-1" />
          )}
          <span>{Math.abs(trend)}% from last period</span>
        </div>
      )}
    </CardContent>
  </Card>
);

// OLAP Operation Badge
const OperationBadge = ({ operation }) => {
  const operationConfig = {
    drill_down: { icon: ArrowDown, color: "bg-blue-500/10 text-blue-600" },
    roll_up: { icon: ArrowUp, color: "bg-green-500/10 text-green-600" },
    slice: { icon: Filter, color: "bg-purple-500/10 text-purple-600" },
    dice: { icon: Layers, color: "bg-orange-500/10 text-orange-600" },
    pivot: { icon: RotateCcw, color: "bg-pink-500/10 text-pink-600" },
    aggregate: { icon: BarChart3, color: "bg-cyan-500/10 text-cyan-600" },
  };

  const config = operationConfig[operation] || operationConfig.aggregate;
  const Icon = config.icon;

  return (
    <Badge className={`${config.color} font-mono text-xs`} data-testid="operation-badge">
      <Icon className="w-3 h-3 mr-1" />
      {operation?.replace(/_/g, " ").toUpperCase()}
    </Badge>
  );
};

// Main Dashboard Component
export default function OLAPDashboard() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [summary, setSummary] = useState(null);
  const [currentResult, setCurrentResult] = useState(null);
  const [darkMode, setDarkMode] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [darkMode]);

  const initializeData = useCallback(async () => {
    try {
      await axios.post(`${API}/data/init`);
      const summaryRes = await axios.get(`${API}/data/summary`);
      setSummary(summaryRes.data);
      toast.success("Data initialized successfully");
    } catch (error) {
      console.error("Error initializing data:", error);
      toast.error("Failed to initialize data");
    }
  }, []);

  useEffect(() => {
    initializeData();
  }, [initializeData]);

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now().toString(),
      role: "user",
      content: inputValue,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setIsLoading(true);

    try {
      const response = await axios.post(`${API}/chat`, {
        message: inputValue,
        session_id: sessionId,
      });

      const assistantMessage = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response.data.response,
        analysis_result: response.data.analysis_result,
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setSessionId(response.data.session_id);

      if (response.data.analysis_result) {
        setCurrentResult(response.data.analysis_result);
      }
    } catch (error) {
      console.error("Error sending message:", error);
      toast.error("Failed to process your query");
      
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "I apologize, but I encountered an error processing your request. Please try again.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const exampleQueries = [
    "Break down Q4 sales by region",
    "Show top 5 products by revenue",
    "Compare sales between North and South",
    "Drill into Q4 by month for Electronics",
    "What's the total sales by category?",
  ];

  return (
    <div className="min-h-screen bg-background" data-testid="olap-dashboard">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-screen-2xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary rounded-sm">
              <BarChart3 className="w-5 h-5 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight">OLAP Assistant</h1>
              <p className="text-xs text-muted-foreground">
                Natural Language Business Analytics
              </p>
            </div>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setDarkMode(!darkMode)}
            data-testid="theme-toggle"
          >
            {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
          </Button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-screen-2xl mx-auto px-6 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Left Sidebar - Chat */}
          <div className="lg:col-span-4 space-y-4">
            <Card className="border-border h-[calc(100vh-200px)] flex flex-col">
              <CardHeader className="pb-3 border-b border-border">
                <CardTitle className="text-base flex items-center gap-2">
                  <MessageSquare className="w-4 h-4" />
                  Query Assistant
                </CardTitle>
              </CardHeader>

              {/* Messages Area */}
              <ScrollArea className="flex-1 p-4" data-testid="chat-messages">
                {messages.length === 0 ? (
                  <div className="text-center py-8">
                    <Sparkles className="w-10 h-10 mx-auto text-primary/50 mb-4" />
                    <p className="text-sm text-muted-foreground mb-4">
                      Ask questions in natural language
                    </p>
                    <div className="space-y-2">
                      {exampleQueries.map((query, idx) => (
                        <button
                          key={idx}
                          onClick={() => setInputValue(query)}
                          className="block w-full text-left px-3 py-2 text-xs font-mono bg-muted hover:bg-muted/80 rounded transition-colors"
                          data-testid={`example-query-${idx}`}
                        >
                          "{query}"
                        </button>
                      ))}
                    </div>
                  </div>
                ) : (
                  messages.map((msg) => <ChatMessage key={msg.id} message={msg} />)
                )}
                {isLoading && (
                  <div className="flex justify-start mb-4">
                    <div className="chat-message-assistant px-4 py-3">
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-primary rounded-full animate-pulse" />
                        <div className="w-2 h-2 bg-primary rounded-full animate-pulse delay-100" />
                        <div className="w-2 h-2 bg-primary rounded-full animate-pulse delay-200" />
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </ScrollArea>

              {/* Input Area */}
              <div className="p-4 border-t border-border">
                <div className="flex gap-2">
                  <Input
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Ask about your sales data..."
                    className="font-mono text-sm"
                    disabled={isLoading}
                    data-testid="query-input"
                  />
                  <Button
                    onClick={sendMessage}
                    disabled={!inputValue.trim() || isLoading}
                    size="icon"
                    data-testid="send-button"
                  >
                    <Send className="w-4 h-4" />
                  </Button>
                </div>
              </div>
            </Card>
          </div>

          {/* Right Content - Results */}
          <div className="lg:col-span-8 space-y-4">
            {/* Summary Cards */}
            {summary && (
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4" data-testid="summary-cards">
                <MetricCard
                  label="Total Records"
                  value={summary.total_records?.toLocaleString() || "0"}
                  icon={Database}
                />
                <MetricCard
                  label="Total Sales"
                  value={`$${(summary.total_sales / 1000000).toFixed(1)}M`}
                  icon={TrendingUp}
                  trend={12}
                />
                <MetricCard
                  label="Units Sold"
                  value={summary.total_quantity?.toLocaleString() || "0"}
                  icon={BarChart3}
                />
                <MetricCard
                  label="Avg Sale"
                  value={`$${summary.avg_sale?.toLocaleString() || "0"}`}
                  icon={Layers}
                />
              </div>
            )}

            {/* Results Card */}
            <Card className="border-border" data-testid="results-card">
              <CardHeader className="pb-3 border-b border-border">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-base">Analysis Results</CardTitle>
                  {currentResult && (
                    <OperationBadge operation={currentResult.operation} />
                  )}
                </div>
                {currentResult && (
                  <div className="flex flex-wrap gap-2 mt-2">
                    <span className="text-xs text-muted-foreground">Dimensions:</span>
                    {currentResult.dimensions?.map((dim) => (
                      <Badge key={dim} variant="secondary" className="text-xs font-mono">
                        {dim}
                      </Badge>
                    ))}
                    {currentResult.filters &&
                      Object.keys(currentResult.filters).length > 0 && (
                        <>
                          <Separator orientation="vertical" className="h-4" />
                          <span className="text-xs text-muted-foreground">Filters:</span>
                          {Object.entries(currentResult.filters).map(([key, value]) => (
                            <Badge
                              key={key}
                              variant="outline"
                              className="text-xs font-mono"
                            >
                              {key}: {String(value)}
                            </Badge>
                          ))}
                        </>
                      )}
                  </div>
                )}
              </CardHeader>
              <CardContent className="p-6">
                {currentResult ? (
                  <div className="space-y-6">
                    {/* Chart */}
                    <ResultsChart
                      data={currentResult.data}
                      dimensions={currentResult.dimensions}
                    />
                    
                    <Separator />
                    
                    {/* Table */}
                    <div>
                      <h3 className="text-sm font-semibold mb-3">Detailed Data</h3>
                      <ResultsTable
                        data={currentResult.data}
                        dimensions={currentResult.dimensions}
                      />
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-16">
                    <BarChart3 className="w-16 h-16 mx-auto text-muted-foreground/30 mb-4" />
                    <h3 className="text-lg font-semibold mb-2">No Analysis Yet</h3>
                    <p className="text-sm text-muted-foreground max-w-md mx-auto">
                      Ask a question in the chat to see your sales data analysis here.
                      Try something like "Break down Q4 sales by region"
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Data Schema Info */}
            {summary?.dimensions && (
              <Card className="border-border" data-testid="schema-card">
                <CardHeader className="pb-3">
                  <CardTitle className="text-base">Available Dimensions</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                    <div>
                      <h4 className="font-semibold text-muted-foreground mb-2">Regions</h4>
                      <div className="flex flex-wrap gap-1">
                        {summary.dimensions.regions?.map((r) => (
                          <Badge key={r} variant="secondary" className="text-xs">
                            {r}
                          </Badge>
                        ))}
                      </div>
                    </div>
                    <div>
                      <h4 className="font-semibold text-muted-foreground mb-2">Products</h4>
                      <div className="flex flex-wrap gap-1">
                        {summary.dimensions.products?.slice(0, 5).map((p) => (
                          <Badge key={p} variant="secondary" className="text-xs">
                            {p}
                          </Badge>
                        ))}
                        {summary.dimensions.products?.length > 5 && (
                          <Badge variant="outline" className="text-xs">
                            +{summary.dimensions.products.length - 5}
                          </Badge>
                        )}
                      </div>
                    </div>
                    <div>
                      <h4 className="font-semibold text-muted-foreground mb-2">Quarters</h4>
                      <div className="flex flex-wrap gap-1">
                        {summary.dimensions.quarters?.map((q) => (
                          <Badge key={q} variant="secondary" className="text-xs">
                            {q}
                          </Badge>
                        ))}
                      </div>
                    </div>
                    <div>
                      <h4 className="font-semibold text-muted-foreground mb-2">Years</h4>
                      <div className="flex flex-wrap gap-1">
                        {summary.dimensions.years?.map((y) => (
                          <Badge key={y} variant="secondary" className="text-xs">
                            {y}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
