export type Campaign = {
  id: string;
  title: string;
  brief: string;
  status: "Completed" | "In progress" | "Draft";
  date: string;
  objective: string;
};

const CAMPAIGNS_STORAGE_KEY = "campaign-strategist-campaigns";

export const demoCampaigns: Campaign[] = [
  {
    id: "daylight",
    title: "Summer at Daylight",
    brief: "A warm, community-first launch for Daylight Coffee seasonal menu.",
    status: "Completed",
    date: "Jun 14, 2024",
    objective: "Brand awareness",
  },
  {
    id: "movement",
    title: "Move with intention",
    brief: "Positioning and content system for a mindful movement studio.",
    status: "In progress",
    date: "Jun 11, 2024",
    objective: "Drive sign-ups",
  },
  {
    id: "growing",
    title: "Good things, growing",
    brief:
      "An optimistic brand campaign for a new generation of home gardeners.",
    status: "Completed",
    date: "Jun 05, 2024",
    objective: "Product launch",
  },
];

function getStoredCampaigns(): Campaign[] {
  if (typeof window === "undefined") {
    return [];
  }

  const storedCampaigns = window.localStorage.getItem(CAMPAIGNS_STORAGE_KEY);

  if (!storedCampaigns) {
    return [];
  }

  try {
    return JSON.parse(storedCampaigns) as Campaign[];
  } catch {
    return [];
  }
}

export async function createCampaign(brief: string): Promise<{ id: string }> {
  const id = `campaign-${Date.now()}`;
  const campaign: Campaign = {
    id,
    title: "New campaign",
    brief,
    status: "In progress",
    date: new Date().toLocaleDateString("en-US", {
      month: "short",
      day: "2-digit",
      year: "numeric",
    }),
    objective: "Campaign strategy",
  };

  const campaigns = [...getStoredCampaigns(), campaign];
  window.localStorage.setItem(CAMPAIGNS_STORAGE_KEY, JSON.stringify(campaigns));

  return { id };
}

export function getCampaign(id: string): Campaign | undefined {
  return [...getStoredCampaigns(), ...demoCampaigns].find(
    (campaign) => campaign.id === id,
  );
}
