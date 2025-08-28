module TopModule
(
  input  logic a,
  input  logic b,
  input  logic c,
  input  logic d,
  output logic out
);

  always @(*) begin
    if (c == 1'b0 && d == 1'b0) begin
      case ({a, b})
        2'b00: out = 1'b1;
        2'b01: out = 1'b1;
        2'b11: out = 1'b0;
        2'b10: out = 1'b1;
        default: out = 1'b0;
      endcase
    end else if (c == 1'b0 && d == 1'b1) begin
      case ({a, b})
        2'b00: out = 1'b1;
        2'b01: out = 1'b0;
        2'b11: out = 1'b0;
        2'b10: out = 1'b1;
        default: out = 1'b0;
      endcase
    end else if (c == 1'b1 && d == 1'b1) begin
      case ({a, b})
        2'b00: out = 1'b0;
        2'b01: out = 1'b1;
        2'b11: out = 1'b1;
        2'b10: out = 1'b1;
        default: out = 1'b0;
      endcase
    end else if (c == 1'b1 && d == 1'b0) begin
      case ({a, b})
        2'b00: out = 1'b1;
        2'b01: out = 1'b1;
        2'b11: out = 1'b0;
        2'b10: out = 1'b0;
        default: out = 1'b0;
      endcase
    end else begin
      out = 1'b0; // Default case for other (c,d) combinations
    end
  end

endmodule