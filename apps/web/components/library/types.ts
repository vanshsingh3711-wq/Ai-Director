export type VideoStatus =
  | "QUEUED"
  | "DOWNLOADING"
  | "TRANSCRIBING"
  | "AI_DIRECTING"
  | "RENDERING"
  | "PUBLISHING"
  | "COMPLETED"
  | "FAILED";

export interface VideoJob {
  id: string;
  user_id: string;
  title: string;
  source_url: string;
  rendered_url?: string | null;
  video_type: "talking_head" | "faceless_short" | "tech_explainer" | "insta_reel";
  status: VideoStatus;
  edit_decision_list?: string | null;
  error_log?: string | null;
  created_at: string;
  updated_at: string;
}

export type StatusFilter = "ALL" | "COMPLETED" | "PROCESSING" | "FAILED";
export type VideoTypeFilter = "ALL" | "faceless_short" | "talking_head" | "tech_explainer" | "insta_reel";
export type ViewMode = "grid" | "list";
