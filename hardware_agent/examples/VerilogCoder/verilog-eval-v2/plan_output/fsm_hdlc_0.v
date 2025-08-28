module TopModule
(
  input  logic clk,
  input  logic reset,
  input  logic in,
  output logic disc,
  output logic flag,
  output logic err
);

  // State definitions
  localparam STATE_IDLE = 4'b0000;
  localparam STATE_1    = 4'b0001;
  localparam STATE_11   = 4'b0010;
  localparam STATE_111  = 4'b0011;
  localparam STATE_1111 = 4'b0100;
  localparam STATE_11111 = 4'b0101;
  localparam STATE_111110 = 4'b0110;
  localparam STATE_FLAG = 4'b0111;
  localparam STATE_DISC = 4'b1000;
  localparam STATE_ERR = 4'b1001;

  // State register
  logic [3:0] state;
  logic [3:0] state_next;

  // Sequential logic for state transition
  always @(posedge clk) begin
    if (reset) begin
      state <= STATE_IDLE;
    end else begin
      state <= state_next;
    end
  end

  // Next state combinational logic
  always @(*) begin
    state_next = state;
    case (state)
      STATE_IDLE: state_next = (in) ? STATE_1 : STATE_IDLE;
      STATE_1: state_next = (in) ? STATE_11 : STATE_IDLE;
      STATE_11: state_next = (in) ? STATE_111 : STATE_IDLE;
      STATE_111: state_next = (in) ? STATE_1111 : STATE_IDLE;
      STATE_1111: state_next = (in) ? STATE_11111 : STATE_IDLE;
      STATE_11111: state_next = (in) ? STATE_111110 : STATE_DISC;
      STATE_111110: state_next = (in) ? STATE_ERR : STATE_FLAG;
      STATE_FLAG: state_next = (in) ? STATE_1 : STATE_IDLE;
      STATE_DISC: state_next = (in) ? STATE_1 : STATE_IDLE;
      STATE_ERR: state_next = (in) ? STATE_ERR : STATE_IDLE;
      default: state_next = STATE_IDLE;
    endcase
  end

  // Output combinational logic
  always @(*) begin
    disc = 1'b0;
    flag = 1'b0;
    err = 1'b0;
    case (state)
      STATE_FLAG: flag = 1'b1;
      STATE_DISC: disc = 1'b1;
      STATE_ERR: err = 1'b1;
    endcase
  end

endmodule