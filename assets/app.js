const DATA_URL = "data/jobs.json";
const OWNER_REPOSITORY_KEY = "scout.owner.repository";
const OWNER_BRANCH_KEY = "scout.owner.branch";

const STATUS_LABELS = {
  applying: "Applying",
  closed: "Closed",
  discovered: "Discovered",
  ineligible: "Ineligible",
  interviewing: "Interviewing",
  needs_reverification: "Reverify",
  offer: "Offer",
  preparing: "Preparing",
  queued: "Queued",
  ready: "Ready",
  rejected: "Skipped",
  submitted: "Submitted",
  verified: "Verified",
  watch: "Watch",
  withdrawn: "Withdrawn",
};

const LANE_LABELS = {
  applied_ai: "Applied AI",
  developer_productivity: "Developer productivity",
  platform: "Platform",
  research_data: "Research data",
  research_software: "Research software",
  scientific_software: "Scientific software",
  visualization_geospatial: "Visualization & geospatial",
  watch: "Watch",
};

const STATUS_ORDER = {
  applying: 0,
  preparing: 0,
  ready: 1,
  queued: 2,
  verified: 3,
  needs_reverification: 4,
  discovered: 5,
  interviewing: 6,
  offer: 7,
  submitted: 8,
  watch: 9,
  withdrawn: 10,
  closed: 11,
  ineligible: 12,
  rejected: 13,
};

const DATE_FORMATTER = new Intl.DateTimeFormat("en-US", {
  month: "short",
  day: "numeric",
  year: "numeric",
});

const elements = {
  activeCount: document.querySelector("#active-count"),
  activeFilters: document.querySelector("#active-filters"),
  averageFit: document.querySelector("#average-fit"),
  country: document.querySelector("#country-filter"),
  deadlineCount: document.querySelector("#deadline-count"),
  emptyReset: document.querySelector("#empty-reset"),
  emptyState: document.querySelector("#empty-state"),
  filters: document.querySelector("#filters"),
  footerSnapshot: document.querySelector("#footer-snapshot"),
  grid: document.querySelector("#job-grid"),
  lane: document.querySelector("#lane-filter"),
  ownerBranch: document.querySelector("#owner-branch"),
  ownerButton: document.querySelector("#owner-mode-button"),
  ownerDialog: document.querySelector("#owner-dialog"),
  ownerError: document.querySelector("#owner-error"),
  ownerRepository: document.querySelector("#owner-repository"),
  priority: document.querySelector("#priority-filter"),
  progressCount: document.querySelector("#progress-count"),
  resultCount: document.querySelector("#result-count"),
  search: document.querySelector("#search"),
  signalCopy: document.querySelector("#signal-copy"),
  signalLink: document.querySelector("#signal-link"),
  signalTitle: document.querySelector("#signal-title"),
  snapshotMeta: document.querySelector("#snapshot-meta"),
  sort: document.querySelector("#sort"),
  status: document.querySelector("#status-filter"),
  template: document.querySelector("#job-card-template"),
};

const state = {
  jobs: [],
  metadata: null,
  owner: {
    repository: localStorage.getItem(OWNER_REPOSITORY_KEY) ?? "",
    branch: localStorage.getItem(OWNER_BRANCH_KEY) ?? "master",
  },
};

function parseDate(value) {
  return value ? new Date(value + "T12:00:00") : null;
}

function formatDate(value) {
  const date = parseDate(value);
  return date ? DATE_FORMATTER.format(date) : "Not listed";
}

function daysUntil(value) {
  const deadline = parseDate(value);
  if (!deadline) {
    return null;
  }

  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 12);
  return Math.ceil((deadline.getTime() - today.getTime()) / 86_400_000);
}

function deadlineDetail(job) {
  if (!job.deadline) {
    return { label: "Not listed", className: "" };
  }

  const formatted = formatDate(job.deadline);
  if (job.status === "submitted") {
    return { label: formatted, className: "" };
  }

  const remaining = daysUntil(job.deadline);
  if (remaining === null) {
    return { label: formatted, className: "" };
  }
  if (remaining < 0) {
    return { label: formatted + " · passed", className: "deadline-past" };
  }
  if (remaining === 0) {
    return { label: formatted + " · today", className: "deadline-urgent" };
  }
  if (remaining <= 14) {
    return {
      label: formatted + " · " + remaining + "d",
      className: "deadline-urgent",
    };
  }
  return { label: formatted, className: "" };
}

function labelForStatus(status) {
  return STATUS_LABELS[status] ?? status.replaceAll("_", " ");
}

function labelForLane(lane) {
  return LANE_LABELS[lane] ?? lane.replaceAll("_", " ");
}

function uniqueSorted(values) {
  return [...new Set(values.filter(Boolean))].sort((left, right) =>
    left.localeCompare(right),
  );
}

function addOptions(select, values, labeler = (value) => value) {
  for (const value of values) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = labeler(value);
    select.append(option);
  }
}

function hydrateFilters() {
  const statusValues = uniqueSorted(state.jobs.map((job) => job.status)).sort(
    (left, right) => (STATUS_ORDER[left] ?? 99) - (STATUS_ORDER[right] ?? 99),
  );
  const priorityValues = uniqueSorted(state.jobs.map((job) => job.priority));
  const laneValues = uniqueSorted(state.jobs.map((job) => job.lane));
  const countryValues = uniqueSorted(state.jobs.map((job) => job.country));

  addOptions(elements.status, statusValues, labelForStatus);
  addOptions(elements.priority, priorityValues, (value) => "Priority " + value);
  addOptions(elements.lane, laneValues, labelForLane);
  addOptions(elements.country, countryValues);
}

function restoreQueryState() {
  const params = new URLSearchParams(window.location.search);
  const allowedSorts = new Set(["recommended", "deadline", "fit", "employer"]);

  elements.search.value = params.get("q") ?? "";
  elements.status.value = params.get("status") ?? "";
  elements.priority.value = params.get("priority") ?? "";
  elements.lane.value = params.get("lane") ?? "";
  elements.country.value = params.get("country") ?? "";
  elements.sort.value = allowedSorts.has(params.get("sort"))
    ? params.get("sort")
    : "recommended";
}

function updateQueryState() {
  const params = new URLSearchParams();
  const pairs = [
    ["q", elements.search.value.trim()],
    ["status", elements.status.value],
    ["priority", elements.priority.value],
    ["lane", elements.lane.value],
    ["country", elements.country.value],
    ["sort", elements.sort.value === "recommended" ? "" : elements.sort.value],
  ];

  for (const [key, value] of pairs) {
    if (value) {
      params.set(key, value);
    }
  }

  const query = params.toString();
  const nextUrl =
    window.location.pathname +
    (query ? "?" + query : "") +
    window.location.hash;
  window.history.replaceState(null, "", nextUrl);
}

function operationalCompare(left, right) {
  const statusDifference =
    (STATUS_ORDER[left.status] ?? 99) - (STATUS_ORDER[right.status] ?? 99);
  if (statusDifference !== 0) {
    return statusDifference;
  }

  if (["applying", "preparing", "ready", "queued"].includes(left.status)) {
    const leftDeadline =
      parseDate(left.deadline)?.getTime() ?? Number.POSITIVE_INFINITY;
    const rightDeadline =
      parseDate(right.deadline)?.getTime() ?? Number.POSITIVE_INFINITY;
    if (leftDeadline !== rightDeadline) {
      return leftDeadline - rightDeadline;
    }
  }

  if (left.fit_score !== right.fit_score) {
    return right.fit_score - left.fit_score;
  }

  return left.employer.localeCompare(right.employer);
}

function sortJobs(jobs) {
  const sorted = [...jobs];
  switch (elements.sort.value) {
    case "deadline":
      return sorted.sort((left, right) => {
        const leftDeadline =
          parseDate(left.deadline)?.getTime() ?? Number.POSITIVE_INFINITY;
        const rightDeadline =
          parseDate(right.deadline)?.getTime() ?? Number.POSITIVE_INFINITY;
        return leftDeadline - rightDeadline || operationalCompare(left, right);
      });
    case "fit":
      return sorted.sort(
        (left, right) =>
          right.fit_score - left.fit_score || operationalCompare(left, right),
      );
    case "employer":
      return sorted.sort(
        (left, right) =>
          left.employer.localeCompare(right.employer) ||
          left.title.localeCompare(right.title),
      );
    default:
      return sorted.sort(operationalCompare);
  }
}

function filteredJobs() {
  const query = elements.search.value.trim().toLocaleLowerCase();
  return sortJobs(
    state.jobs.filter((job) => {
      const searchable = [
        job.employer,
        job.title,
        job.location,
        job.country,
        labelForLane(job.lane),
        job.summary,
        job.next_action,
      ]
        .join(" ")
        .toLocaleLowerCase();

      return (
        (!query || searchable.includes(query)) &&
        (!elements.status.value || job.status === elements.status.value) &&
        (!elements.priority.value || job.priority === elements.priority.value) &&
        (!elements.lane.value || job.lane === elements.lane.value) &&
        (!elements.country.value || job.country === elements.country.value)
      );
    }),
  );
}

function ownerWorkspaceUrl(jobId) {
  if (!state.owner.repository) {
    return "";
  }

  const branch = state.owner.branch
    .split("/")
    .map((segment) => encodeURIComponent(segment))
    .join("/");
  return (
    state.owner.repository +
    "/tree/" +
    branch +
    "/applications/" +
    encodeURIComponent(jobId)
  );
}

function renderCard(job) {
  const fragment = elements.template.content.cloneNode(true);
  const card = fragment.querySelector(".job-card");
  const status = fragment.querySelector(".status-pill");
  const priority = fragment.querySelector(".priority-pill");
  const fitRing = fragment.querySelector(".fit-ring");
  const deadline = fragment.querySelector(".job-deadline");
  const publicLink = fragment.querySelector(".job-link");
  const ownerLink = fragment.querySelector(".job-owner-link");
  const copyButton = fragment.querySelector(".job-copy");

  card.dataset.status = job.status;
  card.id = "job-" + job.id;
  status.textContent = labelForStatus(job.status);
  priority.textContent = "Priority " + job.priority;
  fragment.querySelector(".job-employer").textContent = job.employer;
  fragment.querySelector(".job-title").textContent = job.title;
  fragment.querySelector(".job-summary").textContent = job.summary;
  fragment.querySelector(".job-location").textContent =
    [job.location, job.country].filter(Boolean).join(" · ") || "Not listed";
  fragment.querySelector(".job-lane").textContent = labelForLane(job.lane);
  fragment.querySelector(".job-verified").textContent = job.verified_at
    ? formatDate(job.verified_at)
    : "Needs verification";
  fragment.querySelector(".job-next-action").textContent = job.next_action;

  fitRing.style.setProperty("--fit-angle", job.fit_score * 3.6 + "deg");
  fitRing.setAttribute(
    "aria-label",
    "Fit score " + job.fit_score + " out of 100",
  );
  fragment.querySelector(".fit-value").textContent = job.fit_score;

  const deadlineInfo = deadlineDetail(job);
  deadline.textContent = deadlineInfo.label;
  if (deadlineInfo.className) {
    deadline.classList.add(deadlineInfo.className);
  }

  if (job.url) {
    publicLink.href = job.url;
    publicLink.setAttribute(
      "aria-label",
      "Open posting for " + job.title + " at " + job.employer,
    );
  } else {
    publicLink.removeAttribute("href");
    publicLink.setAttribute("aria-disabled", "true");
    publicLink.textContent = "Source unavailable";
  }

  const workspaceUrl = ownerWorkspaceUrl(job.id);
  if (workspaceUrl) {
    ownerLink.href = workspaceUrl;
    ownerLink.classList.remove("is-hidden");
    ownerLink.setAttribute(
      "aria-label",
      "Open private workspace for " + job.title,
    );
  }

  copyButton.dataset.jobId = job.id;
  copyButton.setAttribute("aria-label", "Copy job ID " + job.id);
  return fragment;
}

function renderActiveFilters() {
  const filters = [
    ["Search", elements.search.value.trim(), "search"],
    [
      "Status",
      elements.status.value ? labelForStatus(elements.status.value) : "",
      "status",
    ],
    ["Priority", elements.priority.value, "priority"],
    [
      "Lane",
      elements.lane.value ? labelForLane(elements.lane.value) : "",
      "lane",
    ],
    ["Country", elements.country.value, "country"],
  ].filter(([, value]) => value);

  elements.activeFilters.replaceChildren();
  for (const [label, value, key] of filters) {
    const chip = document.createElement("span");
    chip.className = "filter-chip";
    chip.append(label + ": " + value);

    const remove = document.createElement("button");
    remove.type = "button";
    remove.dataset.filterKey = key;
    remove.setAttribute(
      "aria-label",
      "Remove " + label.toLocaleLowerCase() + " filter",
    );
    remove.textContent = "×";
    chip.append(remove);
    elements.activeFilters.append(chip);
  }
}

function renderQueue() {
  const jobs = filteredJobs();
  elements.grid.replaceChildren();
  const fragment = document.createDocumentFragment();

  for (const job of jobs) {
    fragment.append(renderCard(job));
  }

  elements.grid.append(fragment);
  elements.grid.setAttribute("aria-busy", "false");
  elements.resultCount.textContent =
    jobs.length + " of " + state.jobs.length + " opportunities";
  elements.emptyState.classList.toggle("is-hidden", jobs.length !== 0);
  elements.grid.classList.toggle("is-hidden", jobs.length === 0);
  renderActiveFilters();
  updateQueryState();
}

function renderSummary() {
  const activeStatuses = new Set([
    "applying",
    "preparing",
    "ready",
    "queued",
    "needs_reverification",
  ]);
  const progressStatuses = new Set(["applying", "preparing", "ready"]);
  const active = state.jobs.filter((job) => activeStatuses.has(job.status)).length;
  const inProgress = state.jobs.filter((job) =>
    progressStatuses.has(job.status),
  ).length;
  const nearDeadline = state.jobs.filter((job) => {
    const remaining = daysUntil(job.deadline);
    return (
      job.status !== "submitted" &&
      remaining !== null &&
      remaining >= 0 &&
      remaining <= 14
    );
  }).length;
  const average =
    state.jobs.reduce((total, job) => total + job.fit_score, 0) /
    state.jobs.length;

  elements.activeCount.textContent = active;
  elements.progressCount.textContent = inProgress;
  elements.deadlineCount.textContent = nearDeadline;
  elements.averageFit.textContent = Math.round(average);
}

function renderSnapshot() {
  const generated = formatDate(state.metadata.generated_at);
  elements.snapshotMeta.replaceChildren();

  const snapshot = document.createElement("span");
  const label = document.createElement("strong");
  label.textContent = "Snapshot";
  snapshot.append(label, " " + generated);

  const count = document.createElement("span");
  count.textContent = state.jobs.length + " reviewed public records";
  const warning = document.createElement("span");
  warning.textContent = "Employer postings remain authoritative";
  elements.snapshotMeta.append(snapshot, count, warning);
  elements.footerSnapshot.textContent = "Public snapshot: " + generated;
}

function renderSignal() {
  const candidate = [...state.jobs]
    .filter(
      (job) =>
        !["submitted", "watch", "closed", "rejected"].includes(job.status),
    )
    .sort(operationalCompare)[0];

  if (!candidate) {
    elements.signalTitle.textContent = "The field is clear.";
    elements.signalCopy.textContent =
      "No active public opportunity needs attention.";
    elements.signalLink.classList.add("is-hidden");
    return;
  }

  const deadline = candidate.deadline
    ? " Deadline " + formatDate(candidate.deadline) + "."
    : "";
  elements.signalTitle.textContent = candidate.title;
  elements.signalCopy.textContent =
    candidate.employer + ". " + candidate.next_action + deadline;
  if (candidate.url) {
    elements.signalLink.href = candidate.url;
    elements.signalLink.classList.remove("is-hidden");
    elements.signalLink.setAttribute(
      "aria-label",
      "Open posting for " + candidate.title + " at " + candidate.employer,
    );
  }
}

function updateOwnerButton() {
  elements.ownerButton.classList.toggle(
    "owner-active",
    Boolean(state.owner.repository),
  );
  elements.ownerButton.lastChild.textContent = state.owner.repository
    ? " Owner mode on"
    : " Owner mode";
}

function openOwnerDialog() {
  elements.ownerRepository.value = state.owner.repository;
  elements.ownerBranch.value = state.owner.branch;
  elements.ownerError.classList.add("is-hidden");
  elements.ownerError.textContent = "";
  elements.ownerDialog.showModal();
  window.requestAnimationFrame(() => elements.ownerRepository.focus());
}

function normalizedRepositoryUrl(value) {
  const trimmed = value
    .trim()
    .replace(/\.git\/?$/, "")
    .replace(/\/$/, "");
  if (!trimmed) {
    return "";
  }

  try {
    const url = new URL(trimmed);
    const parts = url.pathname.split("/").filter(Boolean);
    if (
      url.protocol !== "https:" ||
      url.hostname !== "github.com" ||
      parts.length !== 2
    ) {
      return null;
    }
    return "https://github.com/" + parts[0] + "/" + parts[1];
  } catch {
    return null;
  }
}

function saveOwnerMode() {
  const repository = normalizedRepositoryUrl(elements.ownerRepository.value);
  const branch = elements.ownerBranch.value.trim();

  if (repository === null) {
    elements.ownerError.textContent =
      "Use a repository URL like https://github.com/owner/repository.";
    elements.ownerError.classList.remove("is-hidden");
    return;
  }
  if (!branch || !/^[A-Za-z0-9._/-]+$/.test(branch)) {
    elements.ownerError.textContent =
      "Use a valid branch name containing letters, numbers, dots, underscores, slashes, or hyphens.";
    elements.ownerError.classList.remove("is-hidden");
    return;
  }

  state.owner = { repository, branch };
  if (repository) {
    localStorage.setItem(OWNER_REPOSITORY_KEY, repository);
    localStorage.setItem(OWNER_BRANCH_KEY, branch);
  } else {
    localStorage.removeItem(OWNER_REPOSITORY_KEY);
    localStorage.removeItem(OWNER_BRANCH_KEY);
  }
  updateOwnerButton();
  renderQueue();
  elements.ownerDialog.close();
}

function clearOwnerMode() {
  state.owner = { repository: "", branch: "master" };
  localStorage.removeItem(OWNER_REPOSITORY_KEY);
  localStorage.removeItem(OWNER_BRANCH_KEY);
  elements.ownerRepository.value = "";
  elements.ownerBranch.value = "master";
  updateOwnerButton();
  renderQueue();
  elements.ownerDialog.close();
}

async function copyJobId(button) {
  const jobId = button.dataset.jobId;
  const original = button.textContent;
  try {
    await navigator.clipboard.writeText(jobId);
    button.textContent = "Copied";
  } catch {
    const helper = document.createElement("textarea");
    helper.value = jobId;
    helper.style.position = "fixed";
    helper.style.opacity = "0";
    document.body.append(helper);
    helper.select();
    document.execCommand("copy");
    helper.remove();
    button.textContent = "Copied";
  }
  window.setTimeout(() => {
    button.textContent = original;
  }, 1400);
}

function resetFilters() {
  elements.filters.reset();
  window.requestAnimationFrame(renderQueue);
}

function bindEvents() {
  elements.filters.addEventListener("input", renderQueue);
  elements.filters.addEventListener("change", renderQueue);
  elements.filters.addEventListener("reset", () => {
    window.requestAnimationFrame(renderQueue);
  });
  elements.emptyReset.addEventListener("click", resetFilters);
  elements.ownerButton.addEventListener("click", openOwnerDialog);
  document.querySelector("#save-owner").addEventListener("click", saveOwnerMode);
  document.querySelector("#clear-owner").addEventListener("click", clearOwnerMode);

  elements.activeFilters.addEventListener("click", (event) => {
    const button = event.target.closest("[data-filter-key]");
    if (!button) {
      return;
    }
    const control = elements[button.dataset.filterKey];
    if (control) {
      control.value = "";
      renderQueue();
      control.focus();
    }
  });

  elements.grid.addEventListener("click", (event) => {
    const copyButton = event.target.closest(".job-copy");
    if (copyButton) {
      copyJobId(copyButton);
    }
  });

  elements.ownerDialog.addEventListener("click", (event) => {
    if (event.target === elements.ownerDialog) {
      elements.ownerDialog.close();
    }
  });
}

function renderError(error) {
  console.error(error);
  elements.grid.setAttribute("aria-busy", "false");
  elements.grid.innerHTML = [
    "<article class=\"empty-state\">",
    "<span aria-hidden=\"true\">!</span>",
    "<h3>Scout could not read the field.</h3>",
    "<p>The public snapshot is unavailable or invalid. Try refreshing shortly.</p>",
    "</article>",
  ].join("");
  elements.resultCount.textContent = "Snapshot unavailable";
  elements.signalTitle.textContent = "Signal interrupted.";
  elements.signalCopy.textContent =
    "The static data snapshot could not be loaded.";
}

async function initialize() {
  bindEvents();
  updateOwnerButton();

  try {
    const response = await fetch(DATA_URL, {
      headers: { Accept: "application/json" },
    });
    if (!response.ok) {
      throw new Error("Data request failed with " + response.status);
    }

    const payload = await response.json();
    state.metadata = payload;
    state.jobs = payload.jobs;
    hydrateFilters();
    restoreQueryState();
    renderSummary();
    renderSnapshot();
    renderSignal();
    renderQueue();
  } catch (error) {
    renderError(error);
  }
}

initialize();
