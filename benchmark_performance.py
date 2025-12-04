#!/usr/bin/env python3
"""
Performance benchmark to identify optimization opportunities.
Measures each component's execution time.
"""

import time
import sys
from src.core.lexer import OptimizedLexer
from src.core.parser import OptimizedParser
from src.core.generator import OptimizedBibTeXGenerator, BibEntry


# Sample reference data
SAMPLE_REFERENCES = [
    "Smith, J., and Johnson, M. (2023). Advances in machine learning. Journal of AI Research, 45(3), 234-256.",
    "Brown, A., Lee, S., and White, K. (2022). Natural language processing techniques. IEEE Transactions on Computing, 51(2), 123-145.",
    "Garcia, M., et al. (2021). Deep learning applications. Nature Machine Intelligence, 3(8), 567-589.",
    "Zhang, L. (2020). Computer vision methods. International Conference on Vision, pp. 1001-1020.",
    "Wilson, R., and Taylor, P. (2019). Database optimization strategies. ACM Computing Surveys, 52(4), 78-102.",
]

SAMPLE_TEXT = "\n".join(SAMPLE_REFERENCES * 100)  # 500 references


def benchmark_lexer():
    """Benchmark lexer performance."""
    print("\n" + "="*70)
    print("LEXER BENCHMARK")
    print("="*70)
    
    lexer = OptimizedLexer(SAMPLE_TEXT)
    
    start = time.perf_counter()
    tokens = lexer.tokenize()
    elapsed = time.perf_counter() - start
    
    print(f"✓ Tokenized 500 references in {elapsed:.4f}s")
    print(f"  - Tokens found: {len(tokens)}")
    print(f"  - Speed: {500/elapsed:.0f} refs/sec")
    print(f"  - Average: {elapsed*1000/500:.2f}ms per reference")
    
    return elapsed


def benchmark_parser():
    """Benchmark parser performance."""
    print("\n" + "="*70)
    print("PARSER BENCHMARK")
    print("="*70)
    
    parser = OptimizedParser()
    
    start = time.perf_counter()
    for ref in SAMPLE_REFERENCES * 100:
        parser.parse(ref, use_cache=True)
    elapsed = time.perf_counter() - start
    
    print(f"✓ Parsed 500 references in {elapsed:.4f}s")
    print(f"  - Speed: {500/elapsed:.0f} refs/sec")
    print(f"  - Average: {elapsed*1000/500:.2f}ms per reference")
    print(f"  - Cache hits: {len(parser._cache)} entries cached")
    
    return elapsed


def benchmark_generator():
    """Benchmark generator performance."""
    print("\n" + "="*70)
    print("GENERATOR BENCHMARK")
    print("="*70)
    
    generator = OptimizedBibTeXGenerator()
    entries = [
        BibEntry(
            entry_id=f"ref{i}",
            entry_type="article",
            authors="Smith, J.",
            title="Sample Title",
            journal="Journal Name",
            year="2023",
            volume="45",
            number="3",
            pages="234-256"
        )
        for i in range(500)
    ]
    
    start = time.perf_counter()
    bibtex = generator.generate_batch(entries)
    elapsed = time.perf_counter() - start
    
    print(f"✓ Generated 500 BibTeX entries in {elapsed:.4f}s")
    print(f"  - Speed: {500/elapsed:.0f} refs/sec")
    print(f"  - Average: {elapsed*1000/500:.2f}ms per reference")
    print(f"  - Output size: {len(bibtex)/1024:.1f}KB")
    
    return elapsed


def benchmark_end_to_end():
    """Benchmark complete pipeline."""
    print("\n" + "="*70)
    print("END-TO-END PIPELINE BENCHMARK")
    print("="*70)
    
    parser = OptimizedParser()
    generator = OptimizedBibTeXGenerator()
    
    start = time.perf_counter()
    
    entries = []
    for ref in SAMPLE_REFERENCES * 100:
        parsed = parser.parse(ref, use_cache=True)
        entry = BibEntry(
            entry_id=parsed.entry_id,
            entry_type=parsed.entry_type,
            authors=parsed.authors,
            title=parsed.title,
            journal=parsed.journal,
            year=parsed.year,
            volume=parsed.volume,
            number=parsed.number,
            pages=parsed.pages,
            publisher=parsed.publisher,
            school=parsed.school
        )
        entries.append(entry)
    
    bibtex = generator.generate_batch(entries)
    elapsed = time.perf_counter() - start
    
    print(f"✓ Complete pipeline processed 500 references in {elapsed:.4f}s")
    print(f"  - Speed: {500/elapsed:.0f} refs/sec")
    print(f"  - Average: {elapsed*1000/500:.2f}ms per reference")
    
    return elapsed


def main():
    """Run all benchmarks."""
    print("\n" + "="*70)
    print("BIBLIOGRAPHY GENERATOR - PERFORMANCE BENCHMARKS")
    print("="*70)
    
    lexer_time = benchmark_lexer()
    parser_time = benchmark_parser()
    generator_time = benchmark_generator()
    pipeline_time = benchmark_end_to_end()
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Lexer:        {lexer_time:.4f}s ({500/lexer_time:.0f} refs/sec)")
    print(f"Parser:       {parser_time:.4f}s ({500/parser_time:.0f} refs/sec)")
    print(f"Generator:    {generator_time:.4f}s ({500/generator_time:.0f} refs/sec)")
    print(f"Pipeline:     {pipeline_time:.4f}s ({500/pipeline_time:.0f} refs/sec)")
    print("="*70)
    
    # Recommendations
    print("\n" + "="*70)
    print("OPTIMIZATION RECOMMENDATIONS")
    print("="*70)
    
    if lexer_time > 0.01:
        print("⚠️  Lexer is slower - consider using regex findall instead of finditer")
    else:
        print("✓ Lexer performance is good")
    
    if parser_time > 0.05:
        print("⚠️  Parser cache not very effective - consider improving cache key")
    else:
        print("✓ Parser performance is good")
    
    if generator_time > 0.01:
        print("⚠️  Generator is slower - consider string buffering")
    else:
        print("✓ Generator performance is good")
    
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
