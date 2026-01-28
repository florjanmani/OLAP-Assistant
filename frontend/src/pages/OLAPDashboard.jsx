import { useState, useEffect, useRef, useCallback } from "react";
import axios from "axios";
import { toast } from "sonner";
import * as XLSX from "xlsx";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
} from "@/components/ui/dropdown-menu";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter,
} from "@/components/ui/dialog";
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
  Download,
  Bookmark,
  BookmarkCheck,
  PieChart as PieChartIcon,
  LineChart as LineChartIcon,
  Trash2,
  FileSpreadsheet,
  SlidersHorizontal,
  Plus,
  X,
  HelpCircle,
  Box,
  ArrowRight,
  Maximize2,
  Minimize2,
  Grid3X3,
  History,
  GitCompare,
  FileText,
  Clock,
  ArrowLeftRight,
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
  Legend,
  Area,
  AreaChart,
} from "recharts";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const CHART_COLORS = ["#0047AB", "#FF3B30", "#00C7BE", "#AF52DE", "#FF9500", "#34C759", "#FF2D55", "#5856D6"];

// OLAP Operations data
const OLAP_OPERATIONS = [
  {
    name: "Drill-Down",
    icon: ArrowDown,
    color: "text-blue-600 bg-blue-500/10",
    description: "Navigate from summary to detailed data by moving down the hierarchy.",
    example: "Year → Quarter → Month → Day",
    query: "Drill into Q4 sales by month"
  },
  {
    name: "Roll-Up",
    icon: ArrowUp,
    color: "text-green-600 bg-green-500/10",
    description: "Aggregate data by moving up the hierarchy from detailed to summary.",
    example: "Product → Category → All Products",
    query: "Show total sales by category"
  },
  {
    name: "Slice",
    icon: Filter,
    color: "text-purple-600 bg-purple-500/10",
    description: "Select a single dimension value to create a sub-cube of data.",
    example: "Filter by Region = 'North'",
    query: "Show Q4 sales only"
  },
  {
    name: "Dice",
    icon: Grid3X3,
    color: "text-orange-600 bg-orange-500/10",
    description: "Select multiple dimension values to create a sub-cube.",
    example: "Region IN ('North', 'South') AND Quarter = 'Q4'",
    query: "Compare North and South in Q4"
  },
  {
    name: "Pivot",
    icon: RotateCcw,
    color: "text-pink-600 bg-pink-500/10",
    description: "Rotate the data cube to view data from different perspectives.",
    example: "Swap rows and columns in the view",
    query: "Show products by region instead of region by products"
  }
];

// OLAP Operations Guide Component
const OLAPGuide = ({ onSelectQuery }) => (
  <div className="space-y-4">
    <p className="text-sm text-muted-foreground">
      OLAP (Online Analytical Processing) operations allow you to explore multidimensional data:
    </p>
    <div className="space-y-3">
      {OLAP_OPERATIONS.map((op) => (
        <div key={op.name} className="border border-border rounded-md p-4">
          <div className="flex items-start gap-3">
            <div className={`p-2 rounded-md ${op.color}`}>
              <op.icon className="w-4 h-4" />
            </div>
            <div className="flex-1 min-w-0">
              <h4 className="font-semibold text-sm">{op.name}</h4>
              <p className="text-xs text-muted-foreground mt-1">{op.description}</p>
              <div className="mt-2 flex items-center gap-2 text-xs">
                <span className="text-muted-foreground">Example:</span>
                <code className="bg-muted px-1.5 py-0.5 rounded font-mono">{op.example}</code>
              </div>
              <button
                onClick={() => onSelectQuery(op.query)}
                className="mt-2 text-xs text-primary hover:underline flex items-center gap-1"
                data-testid={`guide-query-${op.name.toLowerCase()}`}
              >
                Try: &quot;{op.query}&quot;
                <ArrowRight className="w-3 h-3" />
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  </div>
);

// Data Cube Visualization Component
const DataCubeVisualization = () => (
  <div className="space-y-4">
    <p className="text-sm text-muted-foreground">
      A data cube represents multidimensional data with dimensions and measures:
    </p>
    
    {/* 3D Cube Visualization */}
    <div className="relative h-64 flex items-center justify-center">
      <svg viewBox="0 0 300 250" className="w-full h-full max-w-[300px]">
        {/* Back face */}
        <polygon 
          points="80,40 220,40 220,140 80,140" 
          fill="hsl(var(--primary) / 0.1)" 
          stroke="hsl(var(--primary))" 
          strokeWidth="2"
        />
        {/* Left face */}
        <polygon 
          points="40,80 80,40 80,140 40,180" 
          fill="hsl(var(--primary) / 0.15)" 
          stroke="hsl(var(--primary))" 
          strokeWidth="2"
        />
        {/* Bottom face */}
        <polygon 
          points="40,180 80,140 220,140 180,180" 
          fill="hsl(var(--primary) / 0.2)" 
          stroke="hsl(var(--primary))" 
          strokeWidth="2"
        />
        {/* Front face */}
        <polygon 
          points="40,80 180,80 180,180 40,180" 
          fill="hsl(var(--primary) / 0.05)" 
          stroke="hsl(var(--primary))" 
          strokeWidth="2"
        />
        {/* Right face */}
        <polygon 
          points="180,80 220,40 220,140 180,180" 
          fill="hsl(var(--primary) / 0.12)" 
          stroke="hsl(var(--primary))" 
          strokeWidth="2"
        />
        {/* Top face */}
        <polygon 
          points="40,80 80,40 220,40 180,80" 
          fill="hsl(var(--primary) / 0.08)" 
          stroke="hsl(var(--primary))" 
          strokeWidth="2"
        />
        
        {/* Dimension labels */}
        <text x="110" y="25" className="text-xs font-semibold fill-primary">TIME</text>
        <text x="235" y="95" className="text-xs font-semibold fill-primary">REGION</text>
        <text x="5" y="135" className="text-xs font-semibold fill-primary">PRODUCT</text>
        
        {/* Center label */}
        <text x="95" y="135" className="text-sm font-bold fill-foreground">SALES</text>
        <text x="85" y="150" className="text-xs fill-muted-foreground">Measures</text>
        
        {/* Grid lines on faces */}
        <line x1="120" y1="40" x2="120" y2="140" stroke="hsl(var(--border))" strokeWidth="1" strokeDasharray="3,3" />
        <line x1="160" y1="40" x2="160" y2="140" stroke="hsl(var(--border))" strokeWidth="1" strokeDasharray="3,3" />
        <line x1="80" y1="70" x2="220" y2="70" stroke="hsl(var(--border))" strokeWidth="1" strokeDasharray="3,3" />
        <line x1="80" y1="100" x2="220" y2="100" stroke="hsl(var(--border))" strokeWidth="1" strokeDasharray="3,3" />
      </svg>
    </div>

    {/* Dimensions Info */}
    <div className="grid grid-cols-3 gap-3">
      <div className="border border-border rounded-md p-3 text-center">
        <div className="w-8 h-8 bg-blue-500/10 rounded-md flex items-center justify-center mx-auto mb-2">
          <Database className="w-4 h-4 text-blue-600" />
        </div>
        <h4 className="font-semibold text-xs">TIME</h4>
        <p className="text-xs text-muted-foreground mt-1">Year, Quarter, Month</p>
      </div>
      <div className="border border-border rounded-md p-3 text-center">
        <div className="w-8 h-8 bg-green-500/10 rounded-md flex items-center justify-center mx-auto mb-2">
          <Layers className="w-4 h-4 text-green-600" />
        </div>
        <h4 className="font-semibold text-xs">REGION</h4>
        <p className="text-xs text-muted-foreground mt-1">North, South, East, West</p>
      </div>
      <div className="border border-border rounded-md p-3 text-center">
        <div className="w-8 h-8 bg-purple-500/10 rounded-md flex items-center justify-center mx-auto mb-2">
          <Box className="w-4 h-4 text-purple-600" />
        </div>
        <h4 className="font-semibold text-xs">PRODUCT</h4>
        <p className="text-xs text-muted-foreground mt-1">Laptop, Phone, etc.</p>
      </div>
    </div>

    {/* Measures */}
    <div className="border border-border rounded-md p-3">
      <h4 className="font-semibold text-sm mb-2 flex items-center gap-2">
        <TrendingUp className="w-4 h-4 text-primary" />
        Measures (Facts)
      </h4>
      <div className="flex flex-wrap gap-2">
        <Badge variant="secondary">Sales Amount ($)</Badge>
        <Badge variant="secondary">Quantity Sold</Badge>
        <Badge variant="secondary">Average Sale</Badge>
      </div>
    </div>
  </div>
);

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
const ResultsTable = ({ data }) => {
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

// Multi-Chart Component
const ResultsCharts = ({ data, dimensions, chartType }) => {
  if (!data || data.length === 0) return null;

  const chartData = data.slice(0, 10).map((item) => ({
    name: dimensions.map((d) => item[d]).join(" - "),
    sales: item.total_sales_amount || 0,
    quantity: item.total_quantity || 0,
    avgSales: item.avg_sales_amount || 0,
  }));

  const renderChart = () => {
    switch (chartType) {
      case "pie":
        return (
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
                outerRadius={120}
                fill="#8884d8"
                dataKey="sales"
              >
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={CHART_COLORS[index % CHART_COLORS.length]} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  background: "hsl(var(--card))",
                  border: "1px solid hsl(var(--border))",
                  borderRadius: "4px",
                }}
                formatter={(value) => [`$${value.toLocaleString()}`, "Sales"]}
              />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        );
      case "line":
        return (
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
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
              <Line type="monotone" dataKey="sales" stroke={CHART_COLORS[0]} strokeWidth={2} dot={{ fill: CHART_COLORS[0] }} />
            </LineChart>
          </ResponsiveContainer>
        );
      case "area":
        return (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
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
              <Area type="monotone" dataKey="sales" stroke={CHART_COLORS[0]} fill={CHART_COLORS[0]} fillOpacity={0.3} />
            </AreaChart>
          </ResponsiveContainer>
        );
      default: // bar
        return (
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
              <Bar dataKey="sales" fill={CHART_COLORS[0]} radius={[2, 2, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        );
    }
  };

  return <div className="h-[300px] w-full">{renderChart()}</div>;
};

// Metric Card Component
const MetricCard = ({ label, value, icon: Icon, trend }) => (
  <Card className="metric-card border-border relative overflow-hidden">
    <CardContent className="p-5 pr-16">
      <p className="metric-label">{label}</p>
      <p className="metric-value mt-1">{value}</p>
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
    <div className="absolute top-5 right-5 w-10 h-10 bg-primary/10 rounded-md flex items-center justify-center">
      <Icon className="w-5 h-5 text-primary" />
    </div>
  </Card>
);

// OLAP Operation Badge with clickable popover
const OperationBadge = ({ operation }) => {
  const operationConfig = {
    drill_down: { 
      icon: ArrowDown, 
      color: "bg-blue-500/10 text-blue-600 hover:bg-blue-500/20",
      name: "Drill-Down",
      description: "Navigate from summary to detailed data by moving down the hierarchy.",
      example: "Year → Quarter → Month → Day"
    },
    roll_up: { 
      icon: ArrowUp, 
      color: "bg-green-500/10 text-green-600 hover:bg-green-500/20",
      name: "Roll-Up",
      description: "Aggregate data by moving up the hierarchy from detailed to summary.",
      example: "Product → Category → All Products"
    },
    slice: { 
      icon: Filter, 
      color: "bg-purple-500/10 text-purple-600 hover:bg-purple-500/20",
      name: "Slice",
      description: "Select a single dimension value to create a sub-cube of data.",
      example: "Filter by Quarter = 'Q4'"
    },
    dice: { 
      icon: Grid3X3, 
      color: "bg-orange-500/10 text-orange-600 hover:bg-orange-500/20",
      name: "Dice",
      description: "Select multiple dimension values to create a sub-cube.",
      example: "Region IN ('North', 'South') AND Quarter = 'Q4'"
    },
    pivot: { 
      icon: RotateCcw, 
      color: "bg-pink-500/10 text-pink-600 hover:bg-pink-500/20",
      name: "Pivot",
      description: "Rotate the data cube to view data from different perspectives.",
      example: "Swap rows and columns in the view"
    },
    aggregate: { 
      icon: BarChart3, 
      color: "bg-cyan-500/10 text-cyan-600 hover:bg-cyan-500/20",
      name: "Aggregate",
      description: "Summarize data by grouping and calculating totals, averages, etc.",
      example: "SUM(sales) GROUP BY region"
    },
  };

  const config = operationConfig[operation] || operationConfig.aggregate;
  const Icon = config.icon;

  return (
    <Popover>
      <PopoverTrigger asChild>
        <button 
          className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold transition-colors cursor-pointer ${config.color}`}
          data-testid="operation-badge"
        >
          <Icon className="w-3 h-3 mr-1" />
          {operation?.replace(/_/g, " ").toUpperCase()}
        </button>
      </PopoverTrigger>
      <PopoverContent className="w-80" align="end">
        <div className="space-y-3">
          <div className="flex items-center gap-2">
            <div className={`p-2 rounded-md ${config.color}`}>
              <Icon className="w-4 h-4" />
            </div>
            <h4 className="font-semibold">{config.name}</h4>
          </div>
          <p className="text-sm text-muted-foreground">{config.description}</p>
          <div className="pt-2 border-t border-border">
            <p className="text-xs text-muted-foreground">Example:</p>
            <code className="text-xs bg-muted px-2 py-1 rounded mt-1 block font-mono">
              {config.example}
            </code>
          </div>
        </div>
      </PopoverContent>
    </Popover>
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
  const [chartType, setChartType] = useState("bar");
  const [bookmarks, setBookmarks] = useState([]);
  const [filterDialogOpen, setFilterDialogOpen] = useState(false);
  const [filters, setFilters] = useState([]);
  const [guideDialogOpen, setGuideDialogOpen] = useState(false);
  const [cubeDialogOpen, setCubeDialogOpen] = useState(false);
  const [historyDialogOpen, setHistoryDialogOpen] = useState(false);
  const [queryHistory, setQueryHistory] = useState([]);
  const [compareDialogOpen, setCompareDialogOpen] = useState(false);
  const [compareItems, setCompareItems] = useState({ item1: "", item2: "", dimension: "region" });
  const [compareResult, setCompareResult] = useState(null);
  const [isComparing, setIsComparing] = useState(false);
  const messagesEndRef = useRef(null);
  const resultsRef = useRef(null);

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

  // Load bookmarks from localStorage
  useEffect(() => {
    const saved = localStorage.getItem("olap-bookmarks");
    if (saved) {
      setBookmarks(JSON.parse(saved));
    }
  }, []);

  // Save bookmarks to localStorage
  useEffect(() => {
    localStorage.setItem("olap-bookmarks", JSON.stringify(bookmarks));
  }, [bookmarks]);

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

  const sendMessage = async (messageText = inputValue) => {
    if (!messageText.trim() || isLoading) return;

    const userMessage = {
      id: Date.now().toString(),
      role: "user",
      content: messageText,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setIsLoading(true);

    const historyId = Date.now().toString();

    try {
      const response = await axios.post(`${API}/chat`, {
        message: messageText,
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

      // Add to query history with results
      setQueryHistory((prev) => {
        const newHistory = [{ 
          id: historyId,
          query: messageText, 
          timestamp: new Date().toISOString(),
          response: response.data.response,
          result: response.data.analysis_result,
          expanded: false
        }, ...prev];
        return newHistory.slice(0, 20); // Keep last 20 queries
      });

    } catch (error) {
      console.error("Error sending message:", error);
      toast.error("Failed to process your query");
      
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "I apologize, but I encountered an error processing your request. Please try again.",
      };
      setMessages((prev) => [...prev, errorMessage]);

      // Add failed query to history
      setQueryHistory((prev) => {
        const newHistory = [{ 
          id: historyId,
          query: messageText, 
          timestamp: new Date().toISOString(),
          response: "Query failed",
          result: null,
          expanded: false
        }, ...prev];
        return newHistory.slice(0, 20);
      });
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

  // Run comparison between two items
  const runComparison = async () => {
    if (!compareItems.item1 || !compareItems.item2) {
      toast.error("Please select both items to compare");
      return;
    }

    setIsComparing(true);
    const query = `Compare sales between ${compareItems.item1} and ${compareItems.item2}`;
    const historyId = Date.now().toString();
    
    try {
      const response = await axios.post(`${API}/chat`, {
        message: query,
        session_id: sessionId,
      });

      if (response.data.analysis_result) {
        setCompareResult(response.data.analysis_result);
      }
      
      // Add to query history with full response
      setQueryHistory((prev) => {
        const newHistory = [{ 
          id: historyId,
          query, 
          timestamp: new Date().toISOString(),
          response: response.data.response,
          result: response.data.analysis_result,
          expanded: false
        }, ...prev];
        return newHistory.slice(0, 20);
      });
      
      toast.success("Comparison complete");
    } catch (error) {
      console.error("Error running comparison:", error);
      toast.error("Failed to run comparison");
      
      // Add failed query to history
      setQueryHistory((prev) => {
        const newHistory = [{ 
          id: historyId,
          query, 
          timestamp: new Date().toISOString(),
          response: "Comparison failed",
          result: null,
          expanded: false
        }, ...prev];
        return newHistory.slice(0, 20);
      });
    } finally {
      setIsComparing(false);
    }
  };

  // Export to PDF
  const exportToPDF = async () => {
    if (!currentResult?.data || currentResult.data.length === 0) {
      toast.error("No data to export");
      return;
    }

    toast.info("Generating PDF report...");

    try {
      const pdf = new jsPDF("p", "mm", "a4");
      const pageWidth = pdf.internal.pageSize.getWidth();
      
      // Title
      pdf.setFontSize(20);
      pdf.setTextColor(0, 71, 171);
      pdf.text("OLAP Analysis Report", pageWidth / 2, 20, { align: "center" });
      
      // Date
      pdf.setFontSize(10);
      pdf.setTextColor(100, 100, 100);
      pdf.text(`Generated: ${new Date().toLocaleString()}`, pageWidth / 2, 28, { align: "center" });
      
      // Operation info
      pdf.setFontSize(12);
      pdf.setTextColor(0, 0, 0);
      pdf.text(`Operation: ${currentResult.operation?.replace(/_/g, " ").toUpperCase() || "ANALYSIS"}`, 15, 40);
      pdf.text(`Dimensions: ${currentResult.dimensions?.join(", ") || "N/A"}`, 15, 48);
      
      if (currentResult.filters && Object.keys(currentResult.filters).length > 0) {
        const filterText = Object.entries(currentResult.filters)
          .map(([k, v]) => `${k}: ${v}`)
          .join(", ");
        pdf.text(`Filters: ${filterText}`, 15, 56);
      }
      
      // Table header
      let yPos = 70;
      const headers = Object.keys(currentResult.data[0]);
      const colWidth = (pageWidth - 30) / headers.length;
      
      pdf.setFillColor(0, 71, 171);
      pdf.rect(15, yPos - 5, pageWidth - 30, 8, "F");
      pdf.setTextColor(255, 255, 255);
      pdf.setFontSize(9);
      
      headers.forEach((header, idx) => {
        const displayHeader = header.replace(/_/g, " ").replace(/\b\w/g, l => l.toUpperCase());
        pdf.text(displayHeader.substring(0, 12), 17 + idx * colWidth, yPos);
      });
      
      // Table data
      yPos += 10;
      pdf.setTextColor(0, 0, 0);
      pdf.setFontSize(8);
      
      currentResult.data.slice(0, 15).forEach((row, rowIdx) => {
        if (rowIdx % 2 === 0) {
          pdf.setFillColor(245, 245, 245);
          pdf.rect(15, yPos - 4, pageWidth - 30, 7, "F");
        }
        
        headers.forEach((header, idx) => {
          let value = row[header];
          if (typeof value === "number") {
            value = value.toLocaleString("en-US", { maximumFractionDigits: 0 });
          }
          pdf.text(String(value).substring(0, 15), 17 + idx * colWidth, yPos);
        });
        yPos += 7;
      });
      
      // Footer
      pdf.setFontSize(8);
      pdf.setTextColor(150, 150, 150);
      pdf.text("OLAP Assistant - Natural Language Business Analytics", pageWidth / 2, 285, { align: "center" });
      
      pdf.save(`olap_report_${new Date().toISOString().slice(0, 10)}.pdf`);
      toast.success("PDF report downloaded");
    } catch (error) {
      console.error("Error generating PDF:", error);
      toast.error("Failed to generate PDF");
    }
  };

  // Toggle history item expanded state
  const toggleHistoryExpanded = (id) => {
    setQueryHistory((prev) =>
      prev.map((item) =>
        item.id === id ? { ...item, expanded: !item.expanded } : item
      )
    );
  };

  // Export to CSV
  const exportToCSV = () => {
    if (!currentResult?.data || currentResult.data.length === 0) {
      toast.error("No data to export");
      return;
    }

    const headers = Object.keys(currentResult.data[0]);
    const csvContent = [
      headers.join(","),
      ...currentResult.data.map((row) =>
        headers.map((h) => {
          const val = row[h];
          return typeof val === "string" && val.includes(",") ? `"${val}"` : val;
        }).join(",")
      ),
    ].join("\n");

    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute("download", `olap_analysis_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    toast.success("Data exported to CSV");
  };

  // Export to Excel
  const exportToExcel = () => {
    if (!currentResult?.data || currentResult.data.length === 0) {
      toast.error("No data to export");
      return;
    }

    const worksheet = XLSX.utils.json_to_sheet(currentResult.data);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "OLAP Analysis");
    
    // Auto-size columns
    const headers = Object.keys(currentResult.data[0]);
    const colWidths = headers.map(h => ({ wch: Math.max(h.length, 15) }));
    worksheet['!cols'] = colWidths;
    
    XLSX.writeFile(workbook, `olap_analysis_${new Date().toISOString().slice(0, 10)}.xlsx`);
    toast.success("Data exported to Excel");
  };

  // Bookmark current query
  const toggleBookmark = () => {
    const lastUserMessage = [...messages].reverse().find((m) => m.role === "user");
    if (!lastUserMessage) return;

    const query = lastUserMessage.content;
    const isBookmarked = bookmarks.includes(query);

    if (isBookmarked) {
      setBookmarks(bookmarks.filter((b) => b !== query));
      toast.success("Bookmark removed");
    } else {
      setBookmarks([...bookmarks, query]);
      toast.success("Query bookmarked");
    }
  };

  const removeBookmark = (query) => {
    setBookmarks(bookmarks.filter((b) => b !== query));
    toast.success("Bookmark removed");
  };

  const isCurrentQueryBookmarked = () => {
    const lastUserMessage = [...messages].reverse().find((m) => m.role === "user");
    return lastUserMessage && bookmarks.includes(lastUserMessage.content);
  };

  // Filter builder functions
  const addFilter = () => {
    setFilters([...filters, { dimension: "", value: "" }]);
  };

  const updateFilter = (index, field, value) => {
    const newFilters = [...filters];
    newFilters[index][field] = value;
    setFilters(newFilters);
  };

  const removeFilter = (index) => {
    setFilters(filters.filter((_, i) => i !== index));
  };

  const applyFilters = () => {
    if (filters.length === 0 || filters.some(f => !f.dimension || !f.value)) {
      toast.error("Please complete all filter fields");
      return;
    }

    // Build natural language query from filters
    const filterDescriptions = filters.map(f => `${f.dimension} is ${f.value}`).join(" and ");
    const query = `Show sales where ${filterDescriptions}`;
    
    setFilterDialogOpen(false);
    sendMessage(query);
  };

  const clearFilters = () => {
    setFilters([]);
  };

  // Get available filter options from summary
  const getFilterOptions = (dimension) => {
    if (!summary?.dimensions) return [];
    switch (dimension) {
      case "region": return summary.dimensions.regions || [];
      case "quarter": return summary.dimensions.quarters || [];
      case "year": return summary.dimensions.years?.map(String) || [];
      case "product": return summary.dimensions.products || [];
      default: return [];
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
          <div className="flex items-center gap-2">
            {/* Filter Builder */}
            <Dialog open={filterDialogOpen} onOpenChange={setFilterDialogOpen}>
              <DialogTrigger asChild>
                <Button variant="outline" size="sm" data-testid="filter-builder-btn">
                  <SlidersHorizontal className="w-4 h-4 mr-2" />
                  Filter Builder
                  {filters.length > 0 && (
                    <Badge className="ml-2 h-5 px-1.5" variant="secondary">
                      {filters.length}
                    </Badge>
                  )}
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-[500px]">
                <DialogHeader>
                  <DialogTitle>Build Custom Filters</DialogTitle>
                </DialogHeader>
                <div className="space-y-4 py-4">
                  {filters.length === 0 ? (
                    <p className="text-sm text-muted-foreground text-center py-4">
                      No filters added. Click "Add Filter" to start.
                    </p>
                  ) : (
                    filters.map((filter, idx) => (
                      <div key={idx} className="flex items-center gap-2">
                        <Select
                          value={filter.dimension}
                          onValueChange={(v) => updateFilter(idx, "dimension", v)}
                        >
                          <SelectTrigger className="w-[140px]" data-testid={`filter-dimension-${idx}`}>
                            <SelectValue placeholder="Dimension" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="region">Region</SelectItem>
                            <SelectItem value="quarter">Quarter</SelectItem>
                            <SelectItem value="year">Year</SelectItem>
                            <SelectItem value="product">Product</SelectItem>
                          </SelectContent>
                        </Select>
                        <span className="text-sm text-muted-foreground">=</span>
                        <Select
                          value={filter.value}
                          onValueChange={(v) => updateFilter(idx, "value", v)}
                          disabled={!filter.dimension}
                        >
                          <SelectTrigger className="flex-1" data-testid={`filter-value-${idx}`}>
                            <SelectValue placeholder="Value" />
                          </SelectTrigger>
                          <SelectContent>
                            {getFilterOptions(filter.dimension).map((opt) => (
                              <SelectItem key={opt} value={String(opt)}>
                                {opt}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => removeFilter(idx)}
                          data-testid={`remove-filter-${idx}`}
                        >
                          <X className="w-4 h-4" />
                        </Button>
                      </div>
                    ))
                  )}
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={addFilter}
                    className="w-full"
                    data-testid="add-filter-btn"
                  >
                    <Plus className="w-4 h-4 mr-2" />
                    Add Filter
                  </Button>
                </div>
                <DialogFooter>
                  <Button variant="outline" onClick={clearFilters} data-testid="clear-filters-btn">
                    Clear All
                  </Button>
                  <Button onClick={applyFilters} disabled={filters.length === 0} data-testid="apply-filters-btn">
                    Apply Filters
                  </Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>

            {currentResult && (
              <>
                {/* Export Dropdown */}
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="outline" size="sm" data-testid="export-dropdown">
                      <Download className="w-4 h-4 mr-2" />
                      Export
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent>
                    <DropdownMenuItem onClick={exportToCSV} data-testid="export-csv-option">
                      <Download className="w-4 h-4 mr-2" />
                      Export as CSV
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={exportToExcel} data-testid="export-excel-option">
                      <FileSpreadsheet className="w-4 h-4 mr-2" />
                      Export as Excel
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={exportToPDF} data-testid="export-pdf-option">
                      <FileText className="w-4 h-4 mr-2" />
                      Export as PDF Report
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={toggleBookmark}
                  data-testid="bookmark-btn"
                >
                  {isCurrentQueryBookmarked() ? (
                    <BookmarkCheck className="w-4 h-4 mr-2 text-primary" />
                  ) : (
                    <Bookmark className="w-4 h-4 mr-2" />
                  )}
                  {isCurrentQueryBookmarked() ? "Saved" : "Save"}
                </Button>
              </>
            )}

            {/* OLAP Guide Dialog */}
            <Dialog open={guideDialogOpen} onOpenChange={setGuideDialogOpen}>
              <DialogTrigger asChild>
                <Button variant="outline" size="sm" data-testid="olap-guide-btn">
                  <HelpCircle className="w-4 h-4 mr-2" />
                  OLAP Guide
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-[550px] max-h-[80vh] overflow-y-auto">
                <DialogHeader>
                  <DialogTitle className="flex items-center gap-2">
                    <HelpCircle className="w-5 h-5" />
                    OLAP Operations Guide
                  </DialogTitle>
                </DialogHeader>
                <OLAPGuide onSelectQuery={(query) => {
                  setInputValue(query);
                  setGuideDialogOpen(false);
                }} />
              </DialogContent>
            </Dialog>

            {/* Data Cube Dialog */}
            <Dialog open={cubeDialogOpen} onOpenChange={setCubeDialogOpen}>
              <DialogTrigger asChild>
                <Button variant="outline" size="sm" data-testid="data-cube-btn">
                  <Box className="w-4 h-4 mr-2" />
                  Data Cube
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-[500px] max-h-[80vh] overflow-y-auto">
                <DialogHeader>
                  <DialogTitle className="flex items-center gap-2">
                    <Box className="w-5 h-5" />
                    Data Cube Visualization
                  </DialogTitle>
                </DialogHeader>
                <DataCubeVisualization />
              </DialogContent>
            </Dialog>

            {/* Query History Dialog */}
            <Dialog open={historyDialogOpen} onOpenChange={setHistoryDialogOpen}>
              <DialogTrigger asChild>
                <Button variant="outline" size="sm" data-testid="history-btn">
                  <History className="w-4 h-4 mr-2" />
                  History
                  {queryHistory.length > 0 && (
                    <Badge className="ml-2 h-5 px-1.5" variant="secondary">
                      {queryHistory.length}
                    </Badge>
                  )}
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-[600px] max-h-[80vh]">
                <DialogHeader>
                  <DialogTitle className="flex items-center gap-2">
                    <History className="w-5 h-5" />
                    Query History
                  </DialogTitle>
                </DialogHeader>
                <ScrollArea className="h-[450px] pr-4">
                  {queryHistory.length === 0 ? (
                    <div className="text-center py-8 text-muted-foreground">
                      <Clock className="w-10 h-10 mx-auto mb-3 opacity-50" />
                      <p className="text-sm">No queries yet</p>
                      <p className="text-xs mt-1">Your query history will appear here</p>
                    </div>
                  ) : (
                    <div className="space-y-3">
                      {queryHistory.map((item, idx) => (
                        <div
                          key={item.id || idx}
                          className="border border-border rounded-md overflow-hidden"
                        >
                          {/* Header - always visible */}
                          <button
                            onClick={() => toggleHistoryExpanded(item.id)}
                            className="w-full p-3 text-left hover:bg-muted/50 transition-colors flex items-start justify-between gap-2"
                            data-testid={`history-item-${idx}`}
                          >
                            <div className="flex-1 min-w-0">
                              <p className="text-sm font-mono truncate">{item.query}</p>
                              <p className="text-xs text-muted-foreground mt-1">
                                {new Date(item.timestamp).toLocaleString()}
                              </p>
                            </div>
                            <div className="flex items-center gap-2">
                              {item.result && (
                                <Badge variant="secondary" className="text-xs">
                                  {item.result.row_count || 0} results
                                </Badge>
                              )}
                              {item.expanded ? (
                                <Minimize2 className="w-4 h-4 text-muted-foreground" />
                              ) : (
                                <Maximize2 className="w-4 h-4 text-muted-foreground" />
                              )}
                            </div>
                          </button>
                          
                          {/* Expanded content */}
                          {item.expanded && (
                            <div className="border-t border-border p-3 bg-muted/30 space-y-3">
                              {/* Response */}
                              <div>
                                <p className="text-xs font-semibold text-muted-foreground mb-1">Response:</p>
                                <p className="text-sm">{item.response || "No response"}</p>
                              </div>
                              
                              {/* Analysis Result */}
                              {item.result && (
                                <>
                                  <Separator />
                                  <div>
                                    <p className="text-xs font-semibold text-muted-foreground mb-2">Analysis Details:</p>
                                    <div className="grid grid-cols-2 gap-2 text-xs">
                                      <div className="bg-background rounded p-2">
                                        <span className="text-muted-foreground">Operation:</span>
                                        <span className="ml-1 font-mono">{item.result.operation?.replace(/_/g, " ").toUpperCase()}</span>
                                      </div>
                                      <div className="bg-background rounded p-2">
                                        <span className="text-muted-foreground">Results:</span>
                                        <span className="ml-1 font-semibold">{item.result.row_count || 0} rows</span>
                                      </div>
                                    </div>
                                    {item.result.dimensions && (
                                      <div className="mt-2 flex flex-wrap gap-1">
                                        <span className="text-xs text-muted-foreground">Dimensions:</span>
                                        {item.result.dimensions.map((dim) => (
                                          <Badge key={dim} variant="secondary" className="text-xs">
                                            {dim}
                                          </Badge>
                                        ))}
                                      </div>
                                    )}
                                    {item.result.filters && Object.keys(item.result.filters).length > 0 && (
                                      <div className="mt-2 flex flex-wrap gap-1">
                                        <span className="text-xs text-muted-foreground">Filters:</span>
                                        {Object.entries(item.result.filters).map(([k, v]) => (
                                          <Badge key={k} variant="outline" className="text-xs">
                                            {k}: {String(v)}
                                          </Badge>
                                        ))}
                                      </div>
                                    )}
                                    
                                    {/* Top results preview */}
                                    {item.result.data && item.result.data.length > 0 && (
                                      <div className="mt-3">
                                        <p className="text-xs text-muted-foreground mb-1">Top Results:</p>
                                        <div className="bg-background rounded p-2 space-y-1">
                                          {item.result.data.slice(0, 3).map((row, ridx) => (
                                            <div key={ridx} className="text-xs font-mono flex justify-between">
                                              <span>{Object.values(row)[0]}</span>
                                              <span className="text-primary font-semibold">
                                                ${(row.total_sales_amount || 0).toLocaleString()}
                                              </span>
                                            </div>
                                          ))}
                                        </div>
                                      </div>
                                    )}
                                  </div>
                                </>
                              )}
                              
                              {/* Action buttons */}
                              <div className="flex gap-2 pt-2">
                                <Button
                                  variant="outline"
                                  size="sm"
                                  onClick={() => {
                                    setInputValue(item.query);
                                    setHistoryDialogOpen(false);
                                  }}
                                  className="flex-1"
                                >
                                  <RotateCcw className="w-3 h-3 mr-1" />
                                  Re-run Query
                                </Button>
                                {item.result && (
                                  <Button
                                    variant="outline"
                                    size="sm"
                                    onClick={() => {
                                      setCurrentResult(item.result);
                                      setHistoryDialogOpen(false);
                                      toast.success("Results loaded from history");
                                    }}
                                  >
                                    Load Results
                                  </Button>
                                )}
                              </div>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </ScrollArea>
                {queryHistory.length > 0 && (
                  <DialogFooter>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setQueryHistory([])}
                      data-testid="clear-history-btn"
                    >
                      Clear History
                    </Button>
                  </DialogFooter>
                )}
              </DialogContent>
            </Dialog>

            {/* Comparison Mode Dialog */}
            <Dialog open={compareDialogOpen} onOpenChange={setCompareDialogOpen}>
              <DialogTrigger asChild>
                <Button variant="outline" size="sm" data-testid="compare-btn">
                  <GitCompare className="w-4 h-4 mr-2" />
                  Compare
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-[600px] max-h-[80vh] overflow-y-auto">
                <DialogHeader>
                  <DialogTitle className="flex items-center gap-2">
                    <GitCompare className="w-5 h-5" />
                    Comparison Mode
                  </DialogTitle>
                </DialogHeader>
                <div className="space-y-4 py-4">
                  <p className="text-sm text-muted-foreground">
                    Compare sales data between two regions or time periods side-by-side.
                  </p>
                  
                  {/* Dimension Selection */}
                  <div>
                    <label className="text-sm font-medium mb-2 block">Compare by:</label>
                    <Select
                      value={compareItems.dimension}
                      onValueChange={(v) => setCompareItems({ ...compareItems, dimension: v, item1: "", item2: "" })}
                    >
                      <SelectTrigger data-testid="compare-dimension">
                        <SelectValue placeholder="Select dimension" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="region">Region</SelectItem>
                        <SelectItem value="quarter">Quarter</SelectItem>
                        <SelectItem value="product">Product</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  {/* Item Selection */}
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="text-sm font-medium mb-2 block">First Item:</label>
                      <Select
                        value={compareItems.item1}
                        onValueChange={(v) => setCompareItems({ ...compareItems, item1: v })}
                      >
                        <SelectTrigger data-testid="compare-item1">
                          <SelectValue placeholder="Select item" />
                        </SelectTrigger>
                        <SelectContent>
                          {compareItems.dimension === "region" && summary?.dimensions?.regions?.map((r) => (
                            <SelectItem key={r} value={r}>{r}</SelectItem>
                          ))}
                          {compareItems.dimension === "quarter" && summary?.dimensions?.quarters?.map((q) => (
                            <SelectItem key={q} value={q}>{q}</SelectItem>
                          ))}
                          {compareItems.dimension === "product" && summary?.dimensions?.products?.map((p) => (
                            <SelectItem key={p} value={p}>{p}</SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    <div>
                      <label className="text-sm font-medium mb-2 block">Second Item:</label>
                      <Select
                        value={compareItems.item2}
                        onValueChange={(v) => setCompareItems({ ...compareItems, item2: v })}
                      >
                        <SelectTrigger data-testid="compare-item2">
                          <SelectValue placeholder="Select item" />
                        </SelectTrigger>
                        <SelectContent>
                          {compareItems.dimension === "region" && summary?.dimensions?.regions?.map((r) => (
                            <SelectItem key={r} value={r}>{r}</SelectItem>
                          ))}
                          {compareItems.dimension === "quarter" && summary?.dimensions?.quarters?.map((q) => (
                            <SelectItem key={q} value={q}>{q}</SelectItem>
                          ))}
                          {compareItems.dimension === "product" && summary?.dimensions?.products?.map((p) => (
                            <SelectItem key={p} value={p}>{p}</SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  {/* Comparison Results */}
                  {compareResult && (
                    <div className="border border-border rounded-md p-4 mt-4">
                      <h4 className="font-semibold text-sm mb-3 flex items-center gap-2">
                        <ArrowLeftRight className="w-4 h-4" />
                        Comparison Results
                      </h4>
                      <div className="grid grid-cols-2 gap-4">
                        {compareResult.data?.slice(0, 2).map((item, idx) => {
                          const itemName = compareItems.dimension === "region" ? item.region :
                                          compareItems.dimension === "quarter" ? item.quarter :
                                          item.product;
                          return (
                            <div key={idx} className="bg-muted/50 rounded-md p-3">
                              <p className="font-semibold text-sm">{itemName || `Item ${idx + 1}`}</p>
                              <p className="text-2xl font-bold mt-1">
                                ${(item.total_sales_amount || 0).toLocaleString()}
                              </p>
                              <p className="text-xs text-muted-foreground">
                                {(item.total_quantity || 0).toLocaleString()} units
                              </p>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  )}
                </div>
                <DialogFooter>
                  <Button
                    onClick={runComparison}
                    disabled={!compareItems.item1 || !compareItems.item2 || isComparing}
                    data-testid="run-compare-btn"
                  >
                    {isComparing ? "Comparing..." : "Run Comparison"}
                  </Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>

            <Button
              variant="ghost"
              size="icon"
              onClick={() => setDarkMode(!darkMode)}
              data-testid="theme-toggle"
            >
              {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-screen-2xl mx-auto px-6 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Left Sidebar - Chat */}
          <div className="lg:col-span-4 space-y-4">
            {/* Bookmarks Card */}
            {bookmarks.length > 0 && (
              <Card className="border-border" data-testid="bookmarks-card">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm flex items-center gap-2">
                    <BookmarkCheck className="w-4 h-4" />
                    Saved Queries ({bookmarks.length})
                  </CardTitle>
                </CardHeader>
                <CardContent className="pt-2">
                  <div className="space-y-1 max-h-32 overflow-y-auto">
                    {bookmarks.map((query, idx) => (
                      <div
                        key={idx}
                        className="flex items-center justify-between gap-2 text-xs font-mono bg-muted rounded px-2 py-1.5 group"
                      >
                        <button
                          onClick={() => sendMessage(query)}
                          className="text-left truncate flex-1 hover:text-primary"
                          data-testid={`bookmark-query-${idx}`}
                        >
                          {query}
                        </button>
                        <button
                          onClick={() => removeBookmark(query)}
                          className="opacity-0 group-hover:opacity-100 text-muted-foreground hover:text-destructive transition-opacity"
                          data-testid={`remove-bookmark-${idx}`}
                        >
                          <Trash2 className="w-3 h-3" />
                        </button>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            <Card className="border-border h-[calc(100vh-280px)] flex flex-col">
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
                    onClick={() => sendMessage()}
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
                  <div className="flex items-center gap-2">
                    {currentResult && (
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="outline" size="sm" data-testid="chart-type-dropdown">
                            {chartType === "bar" && <BarChart3 className="w-4 h-4 mr-2" />}
                            {chartType === "pie" && <PieChartIcon className="w-4 h-4 mr-2" />}
                            {chartType === "line" && <LineChartIcon className="w-4 h-4 mr-2" />}
                            {chartType === "area" && <TrendingUp className="w-4 h-4 mr-2" />}
                            Chart Type
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent>
                          <DropdownMenuItem onClick={() => setChartType("bar")} data-testid="chart-bar">
                            <BarChart3 className="w-4 h-4 mr-2" /> Bar Chart
                          </DropdownMenuItem>
                          <DropdownMenuItem onClick={() => setChartType("pie")} data-testid="chart-pie">
                            <PieChartIcon className="w-4 h-4 mr-2" /> Pie Chart
                          </DropdownMenuItem>
                          <DropdownMenuItem onClick={() => setChartType("line")} data-testid="chart-line">
                            <LineChartIcon className="w-4 h-4 mr-2" /> Line Chart
                          </DropdownMenuItem>
                          <DropdownMenuItem onClick={() => setChartType("area")} data-testid="chart-area">
                            <TrendingUp className="w-4 h-4 mr-2" /> Area Chart
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    )}
                    {currentResult && (
                      <OperationBadge operation={currentResult.operation} />
                    )}
                  </div>
                </div>
                {currentResult && (
                  <div className="flex flex-wrap gap-2 mt-2 items-center">
                    <span className="text-xs text-muted-foreground">Dimensions:</span>
                    {currentResult.dimensions?.map((dim) => (
                      <Popover key={dim}>
                        <PopoverTrigger asChild>
                          <button className="inline-flex items-center rounded-full bg-secondary text-secondary-foreground px-2.5 py-0.5 text-xs font-mono cursor-pointer hover:bg-secondary/80 transition-colors">
                            {dim}
                          </button>
                        </PopoverTrigger>
                        <PopoverContent className="w-64" align="start">
                          <div className="space-y-2">
                            <h4 className="font-semibold text-sm capitalize">{dim} Dimension</h4>
                            <p className="text-xs text-muted-foreground">
                              {dim === "region" && "Geographic area where sales occurred (North, South, East, West, Central)."}
                              {dim === "product" && "Specific product sold (Laptop, Phone, Tablet, etc.)."}
                              {dim === "category" && "Product category grouping (Electronics, Computing, Accessories)."}
                              {dim === "quarter" && "Fiscal quarter of the year (Q1, Q2, Q3, Q4)."}
                              {dim === "month" && "Calendar month when the sale occurred."}
                              {dim === "year" && "Calendar year of the transaction (2023, 2024)."}
                            </p>
                            <div className="pt-2 border-t border-border">
                              <p className="text-xs text-muted-foreground">Data is grouped by this dimension in the analysis.</p>
                            </div>
                          </div>
                        </PopoverContent>
                      </Popover>
                    ))}
                    {currentResult.filters &&
                      Object.keys(currentResult.filters).length > 0 && (
                        <>
                          <Separator orientation="vertical" className="h-4" />
                          <span className="text-xs text-muted-foreground">Filters:</span>
                          {Object.entries(currentResult.filters).map(([key, value]) => (
                            <Popover key={key}>
                              <PopoverTrigger asChild>
                                <button className="inline-flex items-center rounded-full border border-input bg-background px-2.5 py-0.5 text-xs font-mono cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors">
                                  {key}: {String(value)}
                                </button>
                              </PopoverTrigger>
                              <PopoverContent className="w-64" align="start">
                                <div className="space-y-2">
                                  <h4 className="font-semibold text-sm">Filter Applied</h4>
                                  <div className="bg-muted rounded-md p-2">
                                    <p className="text-xs font-mono">
                                      <span className="text-muted-foreground capitalize">{key}</span> = <span className="text-primary font-semibold">{String(value)}</span>
                                    </p>
                                  </div>
                                  <p className="text-xs text-muted-foreground">
                                    Only data matching this filter condition is included in the analysis results.
                                  </p>
                                </div>
                              </PopoverContent>
                            </Popover>
                          ))}
                        </>
                      )}
                  </div>
                )}
              </CardHeader>
              <CardContent className="p-6">
                {currentResult ? (
                  <Tabs defaultValue="chart" className="space-y-4">
                    <TabsList>
                      <TabsTrigger value="chart" data-testid="tab-chart">Chart</TabsTrigger>
                      <TabsTrigger value="table" data-testid="tab-table">Table</TabsTrigger>
                    </TabsList>
                    <TabsContent value="chart">
                      <ResultsCharts
                        data={currentResult.data}
                        dimensions={currentResult.dimensions}
                        chartType={chartType}
                      />
                    </TabsContent>
                    <TabsContent value="table">
                      <ResultsTable data={currentResult.data} />
                    </TabsContent>
                  </Tabs>
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
                          <Popover>
                            <PopoverTrigger asChild>
                              <button className="inline-flex items-center rounded-full border border-input bg-background px-2.5 py-0.5 text-xs cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors">
                                +{summary.dimensions.products.length - 5}
                              </button>
                            </PopoverTrigger>
                            <PopoverContent className="w-64" align="start">
                              <div className="space-y-2">
                                <h4 className="font-semibold text-sm">All Products ({summary.dimensions.products.length})</h4>
                                <div className="flex flex-wrap gap-1">
                                  {summary.dimensions.products.map((p) => (
                                    <Badge key={p} variant="secondary" className="text-xs">
                                      {p}
                                    </Badge>
                                  ))}
                                </div>
                              </div>
                            </PopoverContent>
                          </Popover>
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
