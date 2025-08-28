module TopModule
(
  input  logic clk,
  input  logic reset,
  input  logic s,
  input  logic w,
  output logic z
);

  // State definitions
  localparam STATE_A  = 3'b000;
  localparam STATE_B  = 3'b001;
  localparam STATE_B1 = 3'b010;
  localparam STATE_B2 = 3'b011;
  localparam STATE_Z  = 3'b100;

  // State register
  logic [2:0] state, next_state;
  logic pre_w, pre_pre_w;

  // State transition logic
  always_ff @(posedge clk) begin
    if (reset) begin
      state <= STATE_A;
      pre_w <= 1'b0;
      pre_pre_w <= 1'b0;
    end else begin
      state <= next_state;
      pre_pre_w <= pre_w;
      pre_w <= w;
    end
  end

  // Next state logic
  always @(*) begin
    case (state)
      STATE_A: begin
        if (s)
          next_state = STATE_B;
        else
          next_state = STATE_A;
      end
      STATE_B: begin
        next_state = STATE_B1;
      end
      STATE_B1: begin
        next_state = STATE_B2;
      end
      STATE_B2: begin
        if ((pre_pre_w & pre_w & ~w) || (pre_pre_w & ~pre_w & w) || (~pre_pre_w & pre_w & w))
          next_state = STATE_Z;
        else
          next_state = STATE_B;
      end
      STATE_Z: begin
        next_state = STATE_B1; // Corrected transition
      end
      default: next_state = STATE_A;
    endcase
  end

  // Output logic
  always @(*) begin
    if (state == STATE_Z) begin
      z = 1'b1;
    end else begin
      z = 1'b0;
    end
  end

endmodule