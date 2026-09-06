package solution

import "testing"

func TestReviewRevisionFraming0228(t *testing.T) {
	build := func() (*RevisionGraph, []string) {
		g := NewRevisionGraph()
		root := g.Genesis().Digest
		a, err := g.Add([]string{root}, []Edit{{Path:"a",Content:"one"}})
		if err != nil { t.Fatal(err) }
		b, err := g.Add([]string{root}, []Edit{{Path:"b",Content:"two"}})
		if err != nil { t.Fatal(err) }
		return g, []string{root,a.Digest,b.Digest}
	}
	g1, parents := build()
	first, err := g1.Add(parents, nil)
	if err != nil { t.Fatal(err) }
	g2, sameParents := build()
	second, err := g2.Add(sameParents[:1], []Edit{{Path:sameParents[1],Content:sameParents[2]}})
	if err != nil { t.Fatal(err) }
	if first.Digest == second.Digest {
		t.Fatalf("three parents/no edits and one parent/one edit have identical digest: %s", first.Digest)
	}
}
