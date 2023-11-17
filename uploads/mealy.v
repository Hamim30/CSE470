module mealy(clk,rst,w,z);

input clk,rst,w;

output reg z;

reg  pState,nState;

parameter A=1'b 0, B=1'b 1;

//NSL

always @(*)
begin
	case(pState)
		A: if(w==0) nState=A;
			else nState=B;
		B: if(w==0) nState=A;
			else nState=B;
	endcase		
end

//OL

always @(*)
begin
	case(pState)
		A: if(w==0) z=0;
			else z=0;
		B: if(w==0) z=0;
			else z=1;
	endcase		
end

//PSR

always@(posedge clk,negedge rst)
begin
if(!rst) pState<=A;
else pState<=nState;
end
endmodule