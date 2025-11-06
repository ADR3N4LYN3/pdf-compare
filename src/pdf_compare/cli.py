"""
CLI module - Command-line interface for pdf-compare
"""

import click
import sys
import os
import traceback
from pathlib import Path
from tqdm import tqdm
import colorama
from colorama import Fore, Style

from .comparator import PDFComparator
from . import __version__

# Initialize colorama for Windows support
colorama.init(autoreset=True)


def print_success(msg: str):
    """Print success message in green"""
    click.echo(f"{Fore.GREEN}[OK] {msg}{Style.RESET_ALL}")


def print_error(msg: str):
    """Print error message in red"""
    click.echo(f"{Fore.RED}[ERROR] {msg}{Style.RESET_ALL}", err=True)


def print_info(msg: str):
    """Print info message in blue"""
    click.echo(f"{Fore.CYAN}[INFO] {msg}{Style.RESET_ALL}")


def print_warning(msg: str):
    """Print warning message in yellow"""
    click.echo(f"{Fore.YELLOW}[WARNING] {msg}{Style.RESET_ALL}")


@click.command()
@click.version_option(version=__version__, prog_name="pdf-compare")
@click.argument('pdf1', type=click.Path(exists=True, dir_okay=False))
@click.argument('pdf2', type=click.Path(exists=True, dir_okay=False))
@click.option(
    '--output-diff',
    '-o',
    type=click.Path(dir_okay=False),
    help='Output PDF file with highlighted differences'
)
@click.option(
    '--output-json',
    type=click.Path(dir_okay=False),
    help='Output JSON file with detailed statistics'
)
@click.option(
    '--output-html',
    type=click.Path(dir_okay=False),
    help='Output HTML report with visual comparison'
)
@click.option(
    '--output-images',
    type=click.Path(file_okay=False),
    help='Output directory for difference images'
)
@click.option(
    '--output-text',
    type=click.Path(dir_okay=False),
    help='Output text file with comparison summary'
)
@click.option(
    '--dpi',
    type=int,
    default=150,
    help='Resolution for PDF rendering (default: 150, higher = better quality but slower)'
)
@click.option(
    '--threshold',
    type=int,
    default=0,
    help='Pixel difference threshold 0-255 (default: 0 for exact match)'
)
@click.option(
    '--quiet',
    '-q',
    is_flag=True,
    help='Quiet mode - only output result (0=identical, 1=different)'
)
@click.option(
    '--verbose',
    '-v',
    is_flag=True,
    help='Verbose mode - show detailed statistics'
)
@click.option(
    '--no-progress',
    is_flag=True,
    help='Disable progress bar'
)
def main(pdf1, pdf2, output_diff, output_json, output_html, output_images, output_text,
         dpi, threshold, quiet, verbose, no_progress):
    """
    Compare two PDF files and detect visual differences.

    \b
    Examples:
      pdf-compare file1.pdf file2.pdf
      pdf-compare file1.pdf file2.pdf --output-diff diff.pdf
      pdf-compare file1.pdf file2.pdf --output-json stats.json --verbose
      pdf-compare file1.pdf file2.pdf --threshold 10 --dpi 200
    """

    # Progress callback
    pbar = None

    def progress_callback(current, total):
        nonlocal pbar
        if not quiet and not no_progress:
            if pbar is None:
                pbar = tqdm(total=total, desc="Comparing pages", unit="page")
            pbar.update(1)

    try:
        # Initialize comparator
        comparator = PDFComparator(
            dpi=dpi,
            threshold=threshold,
            progress_callback=progress_callback if not quiet and not no_progress else None
        )

        if not quiet:
            print_info(f"Comparing PDFs...")
            print_info(f"  PDF 1: {pdf1}")
            print_info(f"  PDF 2: {pdf2}")
            print_info(f"  DPI: {dpi}, Threshold: {threshold}")
            print("")

        # Perform comparison
        stats = comparator.compare(pdf1, pdf2)

        # Close progress bar
        if pbar:
            pbar.close()

        # Output results
        if quiet:
            # Quiet mode - just exit code
            sys.exit(comparator.get_exit_code())

        # Print summary
        print("")
        if stats.are_identical:
            print_success("PDFs are IDENTICAL")
        else:
            print_warning("PDFs are DIFFERENT")

        print("")
        print(f"{Fore.CYAN}Summary:{Style.RESET_ALL}")
        print(f"  Overall Similarity: {stats.overall_similarity:.2f}%")
        print(f"  Pages Compared: {stats.pages_compared}")
        print(f"  Identical Pages: {stats.identical_pages}")
        print(f"  Different Pages: {stats.different_pages}")

        # Verbose output
        if verbose and stats.different_pages > 0:
            print("")
            print(f"{Fore.CYAN}Detailed Per-Page Statistics:{Style.RESET_ALL}")
            for ps in stats.page_stats:
                if not ps.is_identical:
                    print(f"  Page {ps.page_number + 1}:")
                    print(f"    Similarity: {ps.similarity_percentage:.2f}%")
                    print(f"    Different Pixels: {ps.different_pixels:,} / {ps.total_pixels:,}")
                    print(f"    Difference Regions: {ps.num_difference_regions}")

        # Generate outputs
        outputs_generated = []

        if output_diff:
            comparator.save_diff_pdf(output_diff)
            outputs_generated.append(f"PDF report: {output_diff}")

        if output_json:
            comparator.save_json_report(output_json)
            outputs_generated.append(f"JSON report: {output_json}")

        if output_html:
            comparator.save_html_report(output_html)
            outputs_generated.append(f"HTML report: {output_html}")

        if output_images:
            os.makedirs(output_images, exist_ok=True)
            comparator.save_diff_images(output_images)
            outputs_generated.append(f"Difference images: {output_images}")

        if output_text:
            comparator.save_text_report(output_text)
            outputs_generated.append(f"Text report: {output_text}")

        if outputs_generated:
            print("")
            print(f"{Fore.CYAN}Outputs generated:{Style.RESET_ALL}")
            for output in outputs_generated:
                print(f"  {Fore.GREEN}[+]{Style.RESET_ALL} {output}")

        # Exit with appropriate code
        sys.exit(comparator.get_exit_code())

    except KeyboardInterrupt:
        if pbar:
            pbar.close()
        print("")
        print_warning("Comparison cancelled by user")
        sys.exit(130)

    except Exception as e:
        if pbar:
            pbar.close()
        print_error(f"Error: {str(e)}")
        if verbose:
            traceback.print_exc()
        sys.exit(2)


if __name__ == '__main__':
    main()
