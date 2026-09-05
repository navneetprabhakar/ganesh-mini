package solution
import "testing"
func TestConsumeBeforeStartPreservesTicket(t *testing.T) {
 b, err := NewTicketBook(5)
 if err != nil { t.Fatal(err) }
 if err := b.Add("future",10); err != nil { t.Fatal(err) }
 ok,err := b.Consume("future",9)
 if err != nil || ok { t.Fatalf("before start: %v %v",ok,err) }
 ok,err = b.Check("future",10)
 if err != nil || !ok { t.Fatalf("premature Consume deleted future ticket: Check at start = %v %v",ok,err) }
}
