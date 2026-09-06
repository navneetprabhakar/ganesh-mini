package solution

import "testing"

func TestReviewDecimalID0234(t *testing.T) {
	i := NewInventory()
	id := "9223372036854775808"
	if err := i.Add(Asset{ID:id,Name:"n",Zone:"z"}); err != nil {
		t.Fatalf("canonical positive decimal string ID rejected: %v", err)
	}
	if got, err := i.Get(id); err != nil || got.ID != id { t.Fatalf("got=%+v err=%v", got, err) }
}
