export interface User {
  id: number;
  username: string;
  email: string;
  status: 'ACTIVE' | 'INACTIVE' | 'SUSPENDED';
  roles: string[];
  created_at?: string;
}

export interface Category {
  id: number;
  name: string;
  description?: string;
}

export interface Product {
  id: number;
  category_id: number;
  category_name?: string;
  name: string;
  price: number;
  quantity?: number;
  stock_quantity?: number;
  description?: string;
  image_url?: string;
}

export interface InventoryItem {
  id: number;
  product_id: number;
  product_name: string;
  stock_quantity: number;
  reserved_quantity: number;
  available_quantity: number;
  location: string;
}

export interface Customer {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  phone?: string;
  created_at?: string;
}

export interface Address {
  id: number;
  customer_id: number;
  address_line1: string;
  address_line2?: string;
  city: string;
  state: string;
  postal_code: string;
  country: string;
  is_default: boolean;
}

export interface Supplier {
  id: number;
  name: string;
  contact_name?: string;
  email?: string;
  phone?: string;
}

export interface PurchaseOrder {
  id: number;
  supplier_id: number;
  supplier_name?: string;
  status: 'DRAFT' | 'ORDERED' | 'RECEIVED' | 'CANCELLED';
  total_amount: number;
  created_at: string;
}

export interface CartItem {
  product_id: number;
  product_name: string;
  unit_price: number;
  quantity: number;
  line_total: number;
}

export interface Cart {
  customer_id: number;
  items: CartItem[];
  subtotal: number;
}

export interface OrderItem {
  id: number;
  product_id: number;
  product_name: string;
  quantity: number;
  unit_price: number;
  line_total: number;
}

export interface Order {
  id: number;
  order_number: string;
  customer_id: number;
  customer_name?: string;
  status: 'PENDING' | 'PAID' | 'PROCESSING' | 'SHIPPED' | 'DELIVERED' | 'CANCELLED';
  subtotal: number;
  tax_amount: number;
  discount_amount: number;
  total_amount: number;
  created_at: string;
  items?: OrderItem[];
}

export interface ExecutiveKPIs {
  total_revenue: number;
  gross_profit: number;
  gross_margin_percentage: number;
  total_orders: number;
  average_order_value: number;
  total_units_sold: number;
  active_customers: number;
  customer_lifetime_value: number;
  inventory_valuation: number;
}

export interface RAGQueryResult {
  query: string;
  answer: string;
  sources: string[];
  retrieved_chunks: Array<{ chunk_id: string; title: string; score: number }>;
}

export interface AgentStep {
  thought: string;
  action: string;
  action_input: any;
  observation: any;
}

export interface AgentQueryResult {
  query: string;
  final_answer: string;
  steps: AgentStep[];
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
  error?: any;
  pagination?: {
    page: number;
    limit: number;
    total: number;
    total_pages: number;
  };
}
