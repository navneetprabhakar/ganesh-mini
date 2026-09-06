package solution

import "testing"

func TestReviewCatalogBoundaries0121(t *testing.T) {
	t.Run("tuple identity", func(t *testing.T) {
		c := NewCatalog()
		for _, a := range []Artifact{
			{Workspace:"a", Namespace:"b\x00c", Alias:"d", URI:"one"},
			{Workspace:"a\x00b", Namespace:"c", Alias:"d", URI:"two"},
		} { if err := c.Put(a); err != nil { t.Fatal(err) } }
		if c.Count() != 2 { t.Fatalf("distinct tuples collided: count=%d", c.Count()) }
	})
	t.Run("pagination overflow", func(t *testing.T) {
		c := NewCatalog()
		for _, key := range []string{"a","b"} {
			if err := c.Put(Artifact{Workspace:key,Namespace:"n",Alias:"x",URI:key}); err != nil { t.Fatal(err) }
		}
		defer func() { if p := recover(); p != nil { t.Errorf("valid pagination panicked: %v", p) } }()
		items, err := c.List(1, int(^uint(0)>>1))
		if err != nil || len(items) != 1 { t.Fatalf("items=%v err=%v", items, err) }
	})
}
