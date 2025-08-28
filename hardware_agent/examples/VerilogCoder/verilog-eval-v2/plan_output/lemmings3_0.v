module TopModule
(
  input  logic clk,
  input  logic areset,
  input  logic bump_left,
  input  logic bump_right,
  input  logic ground,
  input  logic dig,
  output logic walk_left,
  output logic walk_right,
  output logic aaah,
  output logic digging
);

  // State definitions
  localparam WALK_LEFT = 3'b000;
  localparam WALK_RIGHT = 3'b001;
  localparam FALL_LEFT = 3'b010;
  localparam FALL_RIGHT = 3'b011;
  localparam DIG_LEFT = 3'b100;
  localparam DIG_RIGHT = 3'b101;

  // State register
  logic [2:0] state, state_next;

  // State transition logic
  always @(*) begin
    state_next = state; // Default to hold state
    case (state)
      WALK_LEFT: begin
        if (!ground) begin
          state_next = FALL_LEFT;
        end else if (dig) begin
          state_next = DIG_LEFT;
        end else if (bump_left) begin
          state_next = WALK_RIGHT;
        end
      end
      WALK_RIGHT: begin
        if (!ground) begin
          state_next = FALL_RIGHT;
        end else if (dig) begin
          state_next = DIG_RIGHT;
        end else if (bump_right) begin
          state_next = WALK_LEFT;
        end
      end
      FALL_LEFT: begin
        if (ground) begin
          state_next = WALK_LEFT;
        end
      end
      FALL_RIGHT: begin
        if (ground) begin
          state_next = WALK_RIGHT;
        end
      end
      DIG_LEFT: begin
        if (!ground) begin
          state_next = FALL_LEFT;
        end
      end
      DIG_RIGHT: begin
        if (!ground) begin
          state_next = FALL_RIGHT;
        end
      end
    endcase
  end

  // State update logic
  always @(posedge clk or posedge areset) begin
    if (areset) begin
      state <= WALK_LEFT;
    end else begin
      state <= state_next;
    end
  end

  // Output logic
  always @(*) begin
    // Default outputs
    walk_left = 1'b0;
    walk_right = 1'b0;
    aaah = 1'b0;
    digging = 1'b0;

    case (state)
      WALK_LEFT: begin
        walk_left = 1'b1;
      end
      WALK_RIGHT: begin
        walk_right = 1'b1;
      end
      FALL_LEFT, FALL_RIGHT: begin
        aaah = 1'b1;
      end
      DIG_LEFT: begin
        digging = 1'b1;
      end
      DIG_RIGHT: begin
        digging = 1'b1;
      end
    endcase
  end

endmodule