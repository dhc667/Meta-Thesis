from typing import Callable, List, TypeVar
from .interfaces import JsonGenerator, Tokenizer
from .prompts.batch_summary import BatchSummaryResponse, BATCH_SUMMARY_CONTEXT, BATCH_SUMMARY_QUERY
from .prompts.merge_summaries import MergeSummaryResponse, MERGE_SUMMARY_CONTEXT, MERGE_SUMMARY_QUERY

T = TypeVar('T', str, BatchSummaryResponse)

class TopicSummarizer:
    def __init__(self, json_generator: JsonGenerator, tokenizer: Tokenizer, max_tokens_per_batch: int = 3000):
        self.json_generator = json_generator
        self.tokenizer = tokenizer
        self.max_tokens_per_batch = max_tokens_per_batch

    def _create_batches(self, items: List[T], get_text: Callable[[T], str]) -> List[List[T]]:
        """
        Generic method to divide items into batches based on token count.
        
        Args:
            items: List of items to batch (either strings or BatchSummaryResponse)
            get_text: Function to extract text content from an item for token counting
            
        Returns:
            List of batches, where each batch is a list of items
        """
        batches = []
        current_batch = []
        current_token_count = 0

        for item in items:
            text = get_text(item)
            text_token_count = self.tokenizer.count_tokens(text)
            
            if text_token_count > self.max_tokens_per_batch:
                # If a single item exceeds the limit, we'll need to process it separately
                if current_batch:
                    batches.append(current_batch)
                batches.append([item])
                current_batch = []
                current_token_count = 0
            elif current_token_count + text_token_count > self.max_tokens_per_batch:
                # If adding this item would exceed the limit, start a new batch
                batches.append(current_batch)
                current_batch = [item]
                current_token_count = text_token_count
            else:
                # Add to current batch
                current_batch.append(item)
                current_token_count += text_token_count

        if current_batch:
            batches.append(current_batch)

        return batches

    def _summarize_abstract_batch(self, texts: List[str]) -> BatchSummaryResponse:
        """Summarize a single batch of abstracts using the JSON generator."""
        combined_texts = "\n\n".join(texts)
        
        return self.json_generator.json_query(
            context=BATCH_SUMMARY_CONTEXT(),
            query=BATCH_SUMMARY_QUERY(combined_texts),
            expected_schema=BatchSummaryResponse
        ).unwrap()

    def _summarize_summary_batch(self, summaries: List[BatchSummaryResponse]) -> MergeSummaryResponse:
        """Merge a batch of summaries into a single summary."""
        if len(summaries) == 1:
            # Convert BatchSummaryResponse to MergeSummaryResponse for consistent typing
            summary = summaries[0]
            return MergeSummaryResponse(
                topic_title=summary.topic_title,
                topic_description=summary.topic_description
            )

        summaries_text = "\n\n".join([
            f"Topic: {s.topic_title}\nDescription: {s.topic_description}"
            for s in summaries
        ])
        
        return self.json_generator.json_query(
            context=MERGE_SUMMARY_CONTEXT(),
            query=MERGE_SUMMARY_QUERY(summaries_text),
            expected_schema=MergeSummaryResponse
        ).unwrap()

    def _hierarchical_merge(self, summaries: List[BatchSummaryResponse]) -> MergeSummaryResponse:
        """
        Hierarchically merge summaries by creating batches and merging them iteratively
        until we have a single summary.
        """
        current_summaries = summaries

        while len(current_summaries) > 1:
            # Create batches of summaries based on token limits
            summary_batches = self._create_batches(
                current_summaries,
                lambda s: f"Topic: {s.topic_title}\nDescription: {s.topic_description}"
            )
            
            # If we only have one batch, we can merge it directly
            if len(summary_batches) == 1:
                return self._summarize_summary_batch(summary_batches[0])
            
            # Otherwise, merge each batch and continue the process
            new_summaries = []
            for batch in summary_batches:
                merged = self._summarize_summary_batch(batch)
                # Convert MergeSummaryResponse back to BatchSummaryResponse for next iteration
                new_summaries.append(BatchSummaryResponse(
                    topic_title=merged.topic_title,
                    topic_description=merged.topic_description
                ))
            
            current_summaries = new_summaries

        # If we have exactly one summary, convert and return it
        if len(current_summaries) == 1:
            summary = current_summaries[0]
            return MergeSummaryResponse(
                topic_title=summary.topic_title,
                topic_description=summary.topic_description
            )
        
        # This should never happen as we continue the loop while len > 1
        raise ValueError("No summaries to merge")

    def summarize_topics(self, texts: List[str]) -> MergeSummaryResponse:
        """
        Analyze a set of texts to find common themes and topics.
        Uses a hierarchical approach to handle large numbers of texts:
        1. First level: Batch and summarize abstracts
        2. Second level and beyond: Batch and merge summaries until we have a single result
        
        Args:
            texts: List of text abstracts to analyze
            
        Returns:
            MergeSummaryResponse containing the identified topic title and description
        """
        if not texts:
            raise ValueError("No texts provided for summarization")

        # First level: Create batches of abstracts and summarize each batch
        abstract_batches = self._create_batches(texts, lambda x: x)
        
        # If we only have one batch that fits within limits, summarize it directly
        if len(abstract_batches) == 1:
            summary = self._summarize_abstract_batch(abstract_batches[0])
            return MergeSummaryResponse(
                topic_title=summary.topic_title,
                topic_description=summary.topic_description
            )
        
        # Otherwise, summarize each batch and then merge hierarchically
        batch_summaries = [
            self._summarize_abstract_batch(batch)
            for batch in abstract_batches
        ]
        
        # Merge summaries hierarchically
        return self._hierarchical_merge(batch_summaries) 
