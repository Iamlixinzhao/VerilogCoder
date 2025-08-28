// The FSM based on the state diagram provided has 6 states: A, B, C, D, E, and F.

module TopModule
(
  input  logic clk,
  input  logic reset,
  input  logic w,
  output logic z
);

// State encoding
localparam STATE_A = 3'b000;
localparam STATE_B = 3'b001;
localparam STATE_C = 3'b010;
localparam STATE_D = 3'b011;
localparam STATE_E = 3'b100;
localparam STATE_F = 3'b101;

// State register
logic [2:0] state;
logic [2:0] state_next;

// State transition logic
always @(posedge clk) begin
  if (reset) begin
    state <= STATE_A;
  end else begin
    state <= state_next;
  end
end

// Next state logic
always @(*) begin
  state_next = state;
  case (state)
    STATE_A: state_next = (w) ? STATE_B : STATE_A;
    STATE_B: state_next = (w) ? STATE_C : STATE_D;
    STATE_C: state_next = (w) ? STATE_E : STATE_D;
    STATE_D: state_next = (w) ? STATE_F : STATE_A;
    STATE_E: state_next = (w) ? STATE_E : STATE_D;
    STATE_F: state_next = (w) ? STATE_C : STATE_D;
    default: state_next = STATE_A;
  endcase
end

// Output logic using continuous assignment
assign z = (state == STATE_E) || (state == STATE_F);

endmodule