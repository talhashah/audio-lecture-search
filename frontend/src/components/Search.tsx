import { useState } from "react";
import axios from "axios";

export default function Search() {
  type SearchResult = {
    document: string;
    id: string;
  };

  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setHasSearched(true);
    setResults([]);

    try {
      const response = await axios.get(
        `http://localhost:8000/search?query=${encodeURIComponent(query)}`
      );
      console.log("API Response:", response.data);
      const docs = response.data.results?.documents?.flat() || [];
      const ids = response.data.results?.ids?.flat() || [];

      const combined = docs.map((doc: string, i: number) => ({
        document: doc,
        id: ids[i],
      }));

      setResults(combined);
    } catch (error) {
      console.error("Search failed:", error);
    } finally {
      setLoading(false);
    }
  };

  // Very Hacky way to generate the URL for each talk. This is mainly for POC Testing and should be replaced with a proper URL generation logic.
  // Helper function to generate talk URL for each id
  const generateTalkUrl = (id: string): string => {
    // Match content between first underscore and "_transcription"
    var talkUrl = "https://sacredlearning.org";
    const match = id.match(/^(.*?)_transcription_/);
    if (match) {
      const raw = match[1]; // e.g. "real_enemy"
      talkUrl =
        "https://storage.googleapis.com/talhashah-cloudstorage/" + raw + ".mp3";
      console.log("Extracted Url:", talkUrl);
    }
    return talkUrl;
  };

  // Very Hacky way to generate the title for each talk. This is mainly for POC Testing and should be replaced with a proper title generation logic.
  // Helper function to generate talk title for each id
  const generateTalkTitle = (id: string): string => {
    // Match content between first underscore and "_transcription"
    var talkTitle = "Religious Talk";
    const match = id.match(/^[^_]+_([^_]+(?:_[^_]+)*)_transcription/);
    if (match) {
      const raw = match[1]; // e.g. "real_enemy"
      // Convert to Title Case: "real_enemy" → "Real Enemy"
      const typeCased = raw
        .split("_")
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(" ");

      talkTitle = typeCased;
      console.log("Extracted Title:", typeCased);
    }
    return talkTitle;
  };

  return (
    <div className="min-h-screen bg-gray-100 flex justify-center items-start p-6">
      <div className="w-full max-w-3xl min-w-[400px]">
        <h1 className="text-3xl font-bold text-gray-800 mb-6 text-center">
          🔍 Lecture Search
        </h1>

        <div className="flex gap-2 mb-6">
          <input
            type="text"
            placeholder="Search lecture content..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") handleSearch();
            }}
            className="flex-1 p-3 rounded-md border border-gray-700 text-black placeholder-gray-400 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
          />

          <button
            onClick={handleSearch}
            disabled={query.trim().length === 0}
            className={`px-4 py-2 rounded-md transition
              ${
                query.trim().length === 0
                  ? "bg-gray-400 text-white cursor-not-allowed"
                  : "bg-blue-600 text-white hover:bg-blue-700"
              }
            `}
          >
            Search
          </button>
        </div>

        <div className="space-y-4">
          {loading && <p className="text-center text-gray-500">Loading...</p>}

          {!loading && hasSearched && results.length === 0 && (
            <p className="text-gray-600 text-center">
              No results found for "<span className="font-medium">{query}</span>
              ".
            </p>
          )}

          {results.map((result, index) => (
            <a
              key={index}
              href={generateTalkUrl(result.id)} // Use generateUrl to create the link dynamically
              className="block bg-white shadow-md rounded-md p-4 border border-gray-200 hover:bg-gray-50 transition"
              target="_blank"
              rel="noopener noreferrer"
            >
              <p className="mt-2 text-sm text-blue-600">
                View source: {generateTalkTitle(result.id)}
              </p>
              <p className="text-gray-800 whitespace-pre-line">
                {result.document}
              </p>
            </a>
          ))}
        </div>
      </div>
    </div>
  );
}
